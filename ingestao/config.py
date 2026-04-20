import os
from dotenv import load_dotenv

load_dotenv()

USGS_URL = os.getenv('USGS_BASE_URL')

BBOX_BR = {
    "minLon": -73.9854,
    "minLat": -33.7519,
    "maxLon": -34.7931,
    "maxLat": 5.2722
}

API_PARAMS = {
    'format': 'geojson',
    'limit': 20000,
    'orderby': 'time',
    'minmagnitude': '1.0'
}