""" The Mozio Service Providers API allows you to perform basic create, update, delete and fetch operations.
    Most of the endpoints are in a predictable REST API format which allows for easy integration.
    The database in use currently is MongoDB.
"""    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from bson.objectid import ObjectId
from django.conf import settings
from bson.json_util import dumps
import pymongo
import traceback
import requests
import json
import time

DB_CONN = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)

@csrf_exempt
def create_or_get_providers(request):
    """ This method allows us to create a service provider object or fetch all providers data based
    on whether the request is a POST or a GET.

    Structure:    api/v1/providers/

    POST:
    Allows us to Create a Service Provider object. It requires the following parameters
    name: Name of the Service Provider(COMPULSARY)
    email: The email address of the service provider(COMPULSARY)
    phone_number: The phone number of the service provider(COMPULSARY)
    language: The preferred language for the service provider(COMPULSARY)
    currency: The preferred currency for the service provider(COMPULSARY)

    The _id of the newly created Service Provider object is returned as a JSON response 
    on successful creation of the Service Provider object.

    All parameters marked COMPULSARY have to be provided as request parameters for a
    desired response.

    GET:
    Fetches all service provider objects and returns a list of service provider objects 
    as a JSON response. No additional input parameters are required
    """
    try:
        db = DB_CONN[settings.MONGO_DB_NAME]
        providers = db["providers"]

        try:
            info = DB_CONN.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            ###### In case of DB failure #########
            return HttpResponse(dumps({}), 
                content_type="application/json", status=500)

        if request.method == "POST":
            name, email, phone_number, language, currency = ("", ) * 5
            provider_id = ""
            try:
                name = request.POST.get("name",)
                email = request.POST.get("email")
                phone_number = request.POST.get("phone_number")
                language = request.POST.get("language")
                currency = request.POST.get("currency")
            except KeyError:
                ####### Missing request parameters ###########
                return HttpResponse(dumps({}), 
                    content_type="application/json", status=404)
            if None in [name, email, phone_number, language, currency]:
                ####### In case of empty request paramaters ##############
                return HttpResponse(dumps({}), 
                    content_type="application/json", status=400)

            ##########  Email is set as unique index in DB (mongoDB)  #############
            try:
                provider_id = providers.insert_one({
                    "name": name,
                    "email": email,
                    "phone_number": phone_number,
                    "language": language,
                    "currency": currency,
                    }).inserted_id
            except:
                ########## Insert exception #############
                return HttpResponse(dumps({}), 
                    content_type="application/json", status=400)

            return HttpResponse(dumps({"_id": provider_id}), 
                content_type="application/json", status=200)

        elif request.method == "GET":
            providers_list = []
            providers_list = providers.find({})
            return HttpResponse(dumps(providers_list), 
                content_type="application/json", status=200)
    except:
        ######### Unhandled Exceptions ###########
        return HttpResponse(dumps({}), 
            content_type="application/json", status=503)

@csrf_exempt
def manage_provider(request, provider_id=None, action=None):
    """
    This method allows us to fetch a single Service Provider object.
    It also allows us to update and delete single Service Provider objects.

    GET:
                            /api/v1/providers/{provider-object-id}/update/

    Example Structure:      /api/v1/providers/56d9ebb93dff263889ad103a/

    Allows us to fetch a single Service Provider object if it exists
    based on the id specified in the URL itself. No other additional
    request parameters are required.

    POST:

    Operation 1

                            /api/v1/providers/{provider-object-id}/update/

    Example Structure:      /api/v1/providers/56d9ebb93dff263889ad103a/update/

    Allows us to update a Service Provider Object with the id specified in the URL
    itslef(if it exists). The presence of "update" at the end of the URL directs
    the API to perform an update operation.

    It requires the following parameters
    name: Name of the Service Provider(COMPULSARY)
    email: The email address of the service provider(COMPULSARY)
    phone_number: The phone number of the service provider(COMPULSARY)
    language: The preferred language for the service provider(COMPULSARY)
    currency: The preferred currency for the service provider(COMPULSARY)

    The _id of the updated Service Provider object is returned as a JSON response 
    on successful updation of the Service Provider object.

    All parameters marked COMPULSARY have to be provided as request parameters for a
    desired response.

    Operation 2

                            /api/v1/providers/{provider-object-id}/delete/

    Example Structure:      /api/v1/providers/56d9ebb93dff263889ad103a/delete/

    Allows us to delete a Service Provider Object with the id specified in the URL
    itslef(if it exists). The presence of "delete" at the end of the URL directs
    the API to perform an delete operation. No other addtional request parameters
    are required for this operation.
    """
    try:
        db = DB_CONN[settings.MONGO_DB_NAME]
        providers = db["providers"]

        try:
            info = DB_CONN.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            ########### In case of DB Failure ##########
            return HttpResponse(dumps({}), 
                content_type="application/json", status=500)

        if request.method == "GET":
            
            if provider_id is not None:
                provider = []
                try:
                    ########## Fetches a singe Service Provider object ##########3
                    provider = providers.find({"_id": ObjectId(provider_id)}).limit(1)
                    if provider.count() == 0:
                        return HttpResponse(dumps({}), 
                            content_type="application/json", status=404)
                    return HttpResponse(dumps(provider), 
                        content_type="application/json", status=200)
                except:
                    return HttpResponse(dumps({}), 
                        content_type="application/json", status=404)
        elif request.method == "POST":
            if provider_id is not None:
                if action in ["update", "delete"]:
                    if action == "update":
                        name, email, phone_number, language, currency = ("", ) * 5
                        try:
                            name = request.POST.get("name",)
                            email = request.POST.get("email")
                            phone_number = request.POST.get("phone_number")
                            language = request.POST.get("language")
                            currency = request.POST.get("currency")
                        except KeyError:
                            return HttpResponse(dumps({}), 
                                content_type="application/json", status=404)
                        if None in [name, email, phone_number, language, currency]:
                            ####### In case of empty request paramaters ########
                            return HttpResponse(dumps({}), 
                                content_type="application/json", status=400)
                        try:
                            updated_id = providers.update_one({"_id": ObjectId(provider_id)}, { '$set': {
                                "name": name,
                                "email": email,
                                "phone_number": phone_number,
                                "language": language,
                                "currency": currency,
                                }}, upsert=False)
                        except:
                            return HttpResponse(dumps({}), 
                                content_type="application/json", status=400)
                        return HttpResponse(dumps({"id": provider_id}), 
                            content_type="application/json", status=200)
                    elif action == "delete":
                        provider = ""
                        try:
                            provider = providers.delete_one({"_id": ObjectId(provider_id)})
                            if provider.deleted_count == 0:
                                return HttpResponse(dumps({}), 
                                    content_type="application/json", status=404)
                            return HttpResponse(dumps({"deleted": 1}), 
                                content_type="application/json", status=200)
                        except:
                            return HttpResponse(dumps({}), 
                                content_type="application/json", status=404)
            
        return HttpResponse(dumps({"total":1}),
            content_type="application/json", status=400)
    except:
        ######### Unhandled Exceptions ###########
        return HttpResponse(dumps({}), 
            content_type="application/json", status=503)

