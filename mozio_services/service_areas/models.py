from __future__ import unicode_literals

from django.db import models

# Create your models here.

#########################
"""Current DB structure in mongoDB for Polygons:
	
	name: Name of the Service Area(COMPULSARY)
    price: The price of the service area specified by the service provider(COMPULSARY)
    provider_id: The id of the service provider which identifies the provider in the providers 
                 collection(COMPULSARY)
    provider_name: The name of the service provider in the providers collection(COMPULSARY)
    polygon_data: A JSON array consisting of coordinates(array of latitude and longitude) for 
                  specifying the boundaries of a polygon. This follows the GEOJSON format(COMPULSARY)
                  Example: [ [ -73.92165, 40.663843 ], [ -73.9221, 40.664251 ], [ -73.92275, 40.667098 ], 
                             [ -73.92165, 40.663843 ] ]
    
    Example: { "_id" : ObjectId("56d9fa2f3dff263b44a36073"), 
    "provider_id" : ObjectId("56d9cd80ca79d385ded6966e"), 
    "name" : "Block Group 6 360470900006", "price" : 10, 
    "geojson_geometry" : { "type" : "Polygon", "coordinates" : [ [ [ -73.92165, 40.663843 ], [ -73.9221, 40.664251 ], 
    [ -73.92275, 40.667098 ], [ -73.92187, 40.667481 ], [ -73.92097, 40.663953 ], [ -73.92165, 40.663843 ] ] 
    ] }, 
    "provider_name" : "ABC Services" }

"""