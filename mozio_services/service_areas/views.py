""" The Mozio Service Areas API allows you to perform basic create, update, delete and fetch operations.
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
def create_or_get_polygons(request):
    """ This function allows us to create a service area object or fetch all service area data based
    on whether the request is a POST or a GET.

    Structure:    api/v1/polygons/

    POST:
    Allows us to Create a Service Area object. It requires the following parameters
    name: Name of the Service Area(COMPULSARY)
    price: The price of the service area specified by the service provider(COMPULSARY)
    provider_id: The id of the service provider which identifies the provider inthe providers 
                 collection(COMPULSARY)
    polygon_data: A JSON array consisting of coordinates(array of latitude and longitude) for 
                  specifying the boundaries of a polygon. This follows the GEOJSON format(COMPULSARY)
                  Example: [ [ -73.92165, 40.663843 ], [ -73.9221, 40.664251 ], [ -73.92275, 40.667098 ], 
                             [ -73.92165, 40.663843 ] ]

    The _id of the newly created Service Area object is returned as a JSON response 
    on successful creation of the Service Area object.

    All parameters marked COMPULSARY have to be provided as request parameters for a
    desired response.

    GET:
    Fetches all service area objects and returns a list of service area objects 
    as a JSON response. No additional input parameters are required
    """
    try:
        db = DB_CONN[settings.MONGO_DB_NAME]
        polygons = db["polygons"]
        providers = db["providers"]

        try:
            info = DB_CONN.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            ########### In case of DB Failure ##########
            return HttpResponse(dumps({}), 
                content_type="application/json", status=500)

        if request.method == "POST":
            polygon_data, name, price, provider_id, provider_name = ("", ) * 5
            polygon_id = ""
            try:
                name = request.POST.get("name",)
                price = float(request.POST.get("price"))
                provider_id = request.POST.get("provider_id")
                #### if the provider_id is correct fetch provider_name from the providers collection ####
                provider = providers.find({"_id": ObjectId(provider_id)}).limit(1)
                if provider.count() == 0:
                    return HttpResponse(dumps({}), 
                        content_type="application/json", status=404)
                else:
                    for record in provider:
                        provider_name = record["name"]
                        break

                ####### Properly format the polygon boundary data as per the GEOJSON format ##########
                polygon_data = {"type": "Polygon", "coordinates": [ json.loads(request.POST.get("polygon_data"))]}

            except:
                return HttpResponse(dumps({}), 
                    content_type="application/json", status=404)
            if None in [name, price, provider_id, polygon_data, provider_name]:
                return HttpResponse(dumps({}), 
                    content_type="application/json", status=400)
            ##########  Email is set as unique index in DB (mongoDB)  #############
            try:
                polygon_id = polygons.insert_one({
                    "name": name,
                    "price": price,
                    "provider_id": provider_id,
                    "provider_name": provider_name,
                    "geojson_geometry": polygon_data,
                    }).inserted_id
            except:
                return HttpResponse(dumps({}), 
                    content_type="application/json", status=400)

            return HttpResponse(dumps({"_id": polygon_id}), 
                content_type="application/json", status=200)

        elif request.method == "GET":
            polygons_list = []
            polygons_list = polygons.find({})
            return HttpResponse(dumps(polygons_list), 
                content_type="application/json", status=200)
    except:
        ######### Unhandled Exceptions ###########
        return HttpResponse(dumps({}), 
            content_type="application/json", status=503)

@csrf_exempt
def manage_polygon(request, polygon_id=None, action=None):
    """
    This method allows us to fetch a single Service Area object.
    It also allows us to update and delete single Service Area objects.

    GET:
                            /api/v1/polygons/{service_area-object-id}/update/

    Example Structure:      /api/v1/polygons/56d9ebb93dff263889ad103a/

    Allows us to fetch a single Service Area object if it exists
    based on the id specified in the URL itself. No other additional
    request parameters are required.

    POST:

    Operation 1

                            /api/v1/polygons/{service_area-object-id}/update/

    Example Structure:      /api/v1/polygons/56d9ebb93dff263889ad103a/update/

    Allows us to update a Service Area Object with the id specified in the URL
    itslef(if it exists). The presence of "update" at the end of the URL directs
    the API to perform an update operation.

    It requires the following parameters
    name: Name of the Service Area(COMPULSARY)
    price: The price of the service area specified by the service provider(COMPULSARY)
    provider_id: The id of the service provider which identifies the provider inthe providers 
                 collection(COMPULSARY)
    polygon_data: A JSON array consisting of coordinates(array of latitude and longitude) for 
                  specifying the boundaries of a polygon. This follows the GEOJSON format(COMPULSARY)
                  Example: [ [ -73.92165, 40.663843 ], [ -73.9221, 40.664251 ], [ -73.92275, 40.667098 ], 
                             [ -73.92165, 40.663843 ] ]

    The _id of the updated Service Area object is returned as a JSON response 
    on successful updation of the Service Provider object.

    All parameters marked COMPULSARY have to be provided as request parameters for a
    desired response.

    Operation 2

                            /api/v1/polygons/{service_area-object-id}/delete/

    Example Structure:      /api/v1/polygons/56d9ebb93dff263889ad103a/delete/

    Allows us to delete a Service Area Object with the id specified in the URL
    itslef(if it exists). The presence of "delete" at the end of the URL directs
    the API to perform an delete operation. No other addtional request parameters
    are required for this operation.
    """
    try:
        db = DB_CONN[settings.MONGO_DB_NAME]
        providers = db["providers"]
        polygons = db["polygons"]

        try:
            info = DB_CONN.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            ########### In case of DB Failure ##########
            return HttpResponse(dumps({}), 
                content_type="application/json", status=500)

        if request.method == "GET":
            
            if polygon_id is not None:
                provider = []
                try:
                    polygon = polygons.find({"_id": ObjectId(polygon_id)}).limit(1)
                    if polygon.count() == 0:
                        return HttpResponse(dumps({}), 
                            content_type="application/json", status=404)
                    return HttpResponse(dumps(polygon), 
                        content_type="application/json", status=200)
                except:
                    return HttpResponse(dumps({}), 
                        content_type="application/json", status=404)
        elif request.method == "POST":
            if polygon_id is not None:
                if action in ["update", "delete"]:
                    if action == "update":

                        polygon_data, name, price, provider_id, provider_name = ("", ) * 5
                        try:
                            name = request.POST.get("name",)
                            price = float(request.POST.get("price"))
                            provider_id = request.POST.get("provider_id")
                            provider = providers.find({"_id": ObjectId(provider_id)}).limit(1)
                            if provider.count() == 0:
                                return HttpResponse(dumps({}), 
                                    content_type="application/json", status=404)
                            else:
                                for record in provider:
                                    provider_name = record["name"]
                                    break
                            ####### Properly format the polygon boundary data as per the GEOJSON format ##########
                            polygon_data = {"type": "Polygon", "coordinates": [ json.loads(request.POST.get("polygon_data"))]}

                        except Exception,e:
                            return HttpResponse(dumps({}), 
                                content_type="application/json", status=404)
                        if None in [name, price, provider_id, polygon_data]:
                            return HttpResponse(dumps({}), 
                                content_type="application/json", status=400)
                        ##########  Email is set as unique index in DB (mongoDB)  #############
                        try:
                            poly_id = polygons.update_one({"_id": ObjectId(polygon_id)}, { '$set': {
                                "name": name,
                                "price": price,
                                "provider_id": provider_id,
                                "provider_name": provider_name,
                                "geojson_geometry": polygon_data,
                                }}, upsert=False)
                        except:
                            return HttpResponse(dumps({}), 
                                content_type="application/json", status=400)

                        return HttpResponse(dumps({"_id": polygon_id}), 
                            content_type="application/json", status=200)
                    elif action == "delete":
                        polygon = ""
                        try:
                            polygon = polygons.delete_one({"_id": ObjectId(polygon_id)})
                            if polygon.deleted_count == 0:
                                return HttpResponse(dumps({}), 
                                    content_type="application/json", status=404)
                            return HttpResponse(dumps({"deleted": 1}), 
                                content_type="application/json", status=200)
                        except:
                            return HttpResponse(dumps({}), 
                                content_type="application/json", status=404)
            
        return HttpResponse(dumps({}),
            content_type="application/json", status=400)
    except:
        ######### Unhandled Exceptions ###########
        return HttpResponse(dumps({}), 
            content_type="application/json", status=503)

def overlapping_polygons(request):
    """ This function allows us to fetch all service areas which overlap a specified
    coordinate.

    Structure:    api/v1/polygons/overlap

    GET:
    Allows us to fetch all service areas which overlap a specified
    coordinate. It requires the following parameters
    
    lat: The latitude of the given coordinate(COMPULSARY)
    long: The longitude of the given coordinate(COMPULSARY)
                  

    An array of matching Service Area objects is returned as a JSON response 
    if there is an overlap with the given coordinate. Each service area object will contain
    it's name, its price and it's service providers name.

    {
        "name",
        "price",
        "provider_name",
    }

    All parameters marked COMPULSARY have to be provided as request parameters for a
    desired response.
    """
    try:
        db = DB_CONN[settings.MONGO_DB_NAME]
        providers = db["providers"]
        polygons = db["polygons"]

        try:
            info = DB_CONN.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            ########### In case of DB Failure ##########
            return HttpResponse(dumps({}), 
                content_type="application/json", status=500)

        if request.method == "GET":
            
            latitude = float(request.GET.get("lat"))
            longitude = float(request.GET.get("long"))
            overlap_polygons = []
            try:
                ### polygons.find({'geojson_geometry': {'$geoIntersects': {'$geometry': 
                ###    {'type': 'Point', 'coordinates': [lat, long1 ]}}}})
                ####### The geospatial query ###########
                overlap_polygons = polygons.find({
                    "geojson_geometry": {
                                            "$geoIntersects": {
                                                                "$geometry": {
                                                                                "type": "Point", 
                                                                                "coordinates": [latitude, longitude ]
                                                                }
                                            }
                    }
                }, {

                    "name": 1,
                    "price": 1,
                    "provider_name": 1

                })
                if overlap_polygons.count() == 0:
                    return HttpResponse(dumps([]), 
                        content_type="application/json", status=200)
                return HttpResponse(dumps(overlap_polygons), 
                    content_type="application/json", status=200)
            except Exception,e:
                return HttpResponse(dumps({"hi":1}), 
                    content_type="application/json", status=404)
        return HttpResponse(dumps({}),
            content_type="application/json", status=400)
    except:
        ######### Unhandled Exceptions ###########
        return HttpResponse(dumps({}), 
            content_type="application/json", status=503)

def overlapping_polygons_detailed(request):
    """ This function allows us to fetch all service areas which overlap a specified
    coordinate.

    Structure:    api/v1/polygons/overlap

    GET:
    Allows us to fetch all service areas which overlap a specified
    coordinate. It requires the following parameters
    
    lat: The latitude of the given coordinate(COMPULSARY)
    long: The longitude of the given coordinate(COMPULSARY)
                  

    An array of matching Service Area objects is returned as a JSON response 
    if there is an overlap with the given coordinate. Each service area object will contain
    it's name, it's price, it's provder's id, it's service providers name and it's polygon
    boundary coordinates data

    {
        "name",
        "price",
        "provider_name",
        "geojson_geometry,
        "provider_id"

    }

    All parameters marked COMPULSARY have to be provided as request parameters for a
    desired response.
    """
    try:
        db = DB_CONN[settings.MONGO_DB_NAME]
        providers = db["providers"]
        polygons = db["polygons"]

        try:
            info = DB_CONN.server_info()
        except pymongo.errors.ServerSelectionTimeoutError:
            ########### In case of DB Failure ##########
            return HttpResponse(dumps({}), 
                content_type="application/json", status=500)

        if request.method == "GET":
            
            latitude = float(request.GET.get("lat"))
            longitude = float(request.GET.get("long"))
            overlap_polygons = []
            try:
                overlap_polygons = polygons.find({
                    "geojson_geometry": {
                                            "$geoIntersects": {
                                                                "$geometry": {
                                                                                "type": "Point", 
                                                                                "coordinates": [latitude, longitude ]
                                                                }
                                            }
                    }
                })
                if overlap_polygons.count() == 0:
                    return HttpResponse(dumps([]), 
                        content_type="application/json", status=200)
                return HttpResponse(dumps(overlap_polygons), 
                    content_type="application/json", status=200)
            except Exception,e:
                return HttpResponse(dumps({"hi":1}), 
                    content_type="application/json", status=404)
        return HttpResponse(dumps({}),
            content_type="application/json", status=400)
    except:
        ######### Unhandled Exceptions ###########
        return HttpResponse(dumps({}), 
            content_type="application/json", status=503)
    

