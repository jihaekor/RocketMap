import json
import logging
import math
from overpy import Overpass
from geofence import Geofences
from models import Gym, init_database
from utils import get_args
from s2sphere import LatLng, Cap, RegionCoverer

args = get_args
app = None
log = logging.getLogger(__name__)
db = init_database(app)
earthCircumferenceMeters = 1000 * 40075.017


def earthMetersToRadians(meters):
    return (2 * math.pi) * (float(meters) / earthCircumferenceMeters)


def ex_query(s, w, n, e):

    # Query Overpass for known gym areas
    api = Overpass()
    result = api.query("""
    [out:json]
    [date:"2016-07-10T00:00:00Z"]
    [timeout:620]
    [bbox:{},{},{},{}];
    (
    //Tags that are confirmed to classify gyms as 'parks' for EX Raids
        way[leisure=park];
        way[landuse=recreation_ground];
        way[leisure=recreation_ground];
        way[leisure=pitch];
        way[leisure=garden];
        way[leisure=golf_course];
        way[leisure=playground];
        way[landuse=meadow];
        way[landuse=grass];
        way[landuse=greenfield];
        way[natural=scrub];
        way[natural=grassland];
        way[landuse=farmyard];
    );
    out body;
    >;
    out skel qt;
    """.format(s, w, n, e))

    return result


def exgyms(geofence):
    # Parse geofence file
    log.info('Finding border points from geofence')
    f = json.loads(json.dumps(Geofences.parse_geofences_file(geofence, '')))
    fence = f[0]['polygon']
    # Figure out borders for bounding box
    south = min(fence, key=lambda ev: ev['lat'])['lat']
    west = min(fence, key=lambda ev: ev['lon'])['lon']
    north = max(fence, key=lambda ev: ev['lat'])['lat']
    east = max(fence, key=lambda ev: ev['lon'])['lon']
    log.info('Finding parks within zone')
    ex_gyms = ex_query(south, west, north, east)

    gyms = Gym.get_gyms(south, west, north, east)
    log.info('Checking {} gyms against {} parks'.format(len(gyms),
                                                        len(ex_gyms.ways)))

    for gym in gyms.items():
        gympoint = {'lat': float(gym[1]['latitude']),
                    'lon': float(gym[1]['longitude'])}
        # get s2 cell corners for each gym
        s2_center = get_s2_cell_center(
                     gympoint['lat'], gympoint['lon'], 0, 20)

        for way in ex_gyms.ways:
            data = []
            for node in way.nodes:
                data.append({'lat': float(node.lat),
                             'lon': float(node.lon)})
            if Geofences.is_point_in_polygon_custom(s2_center, data):
                # Try to get Gym name, but default to id if missing
                try:
                    gymname = Gym.get_gym(gym[0])['name'].encode(
                        'utf8')
                except AttributeError:
                    gymname = gym[0]
                log.info('{} is eligible for EX raid'.format(gymname))
                Gym.is_gym_park(gym[0], True)
                break


def get_s2_cell_center(lat, lng, radius, parent_level):
    radius_radians = earthMetersToRadians(radius)
    latlng = LatLng.from_degrees(float(lat),
                                 float(lng)).normalized().to_point()
    region = Cap.from_axis_height(latlng, (radius_radians*radius_radians)/2)
    coverer = RegionCoverer()
    coverer.min_level = int(parent_level)
    coverer.max_level = int(parent_level)
    coverer.max_cells = 1
    covering = coverer.get_covering(region)
    center = covering[0].to_lat_lng()
    return {'lat': float(center.lat().degrees),
            'lon': float(center.lng().degrees)}
