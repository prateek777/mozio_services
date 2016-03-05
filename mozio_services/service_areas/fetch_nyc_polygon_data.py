import requests
import pymongo

DB_CONN = pymongo.MongoClient(host='localhost', port=27017)

def dump_nyc_data():
    """ Used for fetching 2010 Census Block Groups Polygons
    GEOJSON data from http://data.beta.nyc/dataset/2010-census-block-groups-polygons
    so as to use a sample dataset of polygonsfor testing purposes.

    It Fetches the polygon data and dumps service_area objects in the DB.
    """
    
    db = DB_CONN["mozio_testing"]
    polygons = db["polygons"]
    providers = db["providers"]
    provider_data = []

    try:
        info = DB_CONN.server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
        return

    url = "http://data.beta.nyc//dataset/75ac8522-fec3-47df-8c2f-b45aef1647e9/resource/d2cf6fe5-1914-474e-8648-085ca7067bde/download/da3652503b244838a41c4c2d2de7ecfe2010censusblockgroupspolygonssimple.geojson"
    
    polygon_data = requests.get(url).json()

    providers_list = providers.find({})

    for provider in providers_list:
        p_data = {}
        p_data["provider_id"] = provider["_id"]
        p_data["name"] = provider["name"]
        provider_data.append(p_data)

    count = 0
    for data in polygon_data["features"]:

        if count > 2:
            count = 0

        service_area = {}
        service_area["geojson_geometry"] = data["geometry"]
        service_area["name"] = "%s %s" % (data["properties"]["NAMELSAD"], data["properties"]["GEOID"])
        service_area["price"] = 10
        service_area["provider_id"] = provider_data[count]["provider_id"]
        service_area["provider_name"] = provider_data[count]["name"]

        try:
            polygon_id = polygons.insert_one(service_area).inserted_id
        except:
            continue

        count = count + 1

if __name__ == '__main__':
    dump_nyc_data()

