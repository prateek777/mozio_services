# mozio_services
Mozio Service Provider Service

""" The Mozio Service Providers API allows you to perform basic create, update, delete and fetch operations.
    Most of the endpoints are in a predictable REST API format which allows for easy integration.
    The database in use currently is MongoDB.
"""    


create_or_get_providers()
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
    
manage_provider()
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
    
Mozio Polygon Service

""" The Mozio Service Areas API allows you to perform basic create, update, delete and fetch operations.
    It also allows you to find out exisiting service providers and prices on a particular coordinate.
    Most of the endpoints are in a predictable REST API format which allows for easy integration.
    The database in use currently is MongoDB.
"""   


create_or_get_polygons()
""" This method allows us to create a service area object or fetch all service area data based
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
    
manage_polygon()
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
    
overlapping_polygons()
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
    
overlapping_polygons_detailed
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
