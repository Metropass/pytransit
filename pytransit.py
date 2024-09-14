import socket
import requests
import time
import datetime
#import Exception
from enum import Enum
from json import JSONDecodeError




class TransitObj:
    # The verification functions, just to avoid any errors
    def __checkString(self, value):
        if (isinstance(value, str) is False):
            raise self.NotAStringException(value)
        else:
            return True
    def __checkBool(self, value):
        if (isinstance(value, bool) is False):
            raise self.NotABoolException(value)
        else:
            return True
    def __checkInt(self, value):
        if (isinstance(value, int) is False):
            raise self.NotAnIntException(value)
        else:
            return True
    def __checkFloat(self, value):
        if (type(value) is not type(float)):
            raise self.NotAFloatException
        else:
            return True
    def __constructListOfStops(self, stop_lists):
        sp_list = []
        #print(stop_lists)
        for s in stop_lists:
            sp_list.append(self.Stop(None, s["global_stop_id"], s["location_type"], s["parent_station_global_stop_id"], s["route_type"], s["stop_lat"], s["stop_lon"], s["stop_name"], s["stop_code"], s["rt_stop_id"], s["wheelchair_boarding"]))
        return sp_list
    def __constructListOfItineraries(self, iti_lists):
        it_list = []
        for i in iti_lists:
            it_list.append(self.Itinerary(i["direction_id"], i["headsign"], i["direction_headsign"], i["merged_headsign"], self.__constructListOfScheduleItems(i["schedule_items"]), i["branch_code"]))
        return it_list
    def __constructListOfItineraryDetails(self,itde_lists):
        itd_list = []
        for i in itde_lists:
            itd_list.append(self.ItineraryDetail(i["direction_headsign"], i["direction_id"], i["headsign"], i["merged_headsign"], i["shape"], self.__constructListOfStops(i["stops"]), None, i["canonical_itinerary"], i["is_active"]))
        return itd_list
    def __constructListOfSearchQueryResults(self, query_list):
        q_list = []
        for q in query_list:
            q_list.append(self.SearchQueryResults(q["global_stop_id"], q["location_type"], q["match_strength"], q["parent_station_global_stop_id"], q["route_type"], q["stop_lat"], q["stop_lon"], q["stop_name"]))
        return q_list
    
    '''
    TODO, add an if statement / try statement and merge the schedule item functions together, using KeyError iff we need to use the truncated version of the object
    '''
    def __constructListOfTruncatedScheduleItems(self, sch_items):
        s_items = []
        for s in sch_items:
           s_items.append(self.TruncatedScheduleItem(s["departure_time"], s["stop"]))
        return s_items
    def __constructListOfScheduleItems(self, sch_items):
        s_items = []
        for s in sch_items:
           s_items.append(self.ScheduleItem(s["departure_time"], s["is_cancelled"], s["is_real_time"], s["rt_trip_id"], s["scheduled_departure_time"], s["wheelchair_accessible"], s["trip_search_key"]))
        return s_items
        
    def __constructCustomRoute(self, route_items):
        r_items = None
        try:
            r_items = (self.Route(route_items["global_route_id"], route_items["itineraries"], route_items["route_long_name"], route_items["route_short_name"], route_items["route_type"], route_items["route_color"], route_items["route_text_color"], route_items["route_network_name"], route_items["route_network_id"], route_items["tts_long_name"], route_items["tts_short_name"], route_items["sorting_key"], route_items["mode_name"], route_items["real_time_route_id"]))
        except KeyError:
            r_items = (self.Route(route_items["global_route_id"], None, route_items["route_long_name"], route_items["route_short_name"], route_items["route_type"], route_items["route_color"], route_items["route_text_color"], None, None, route_items["tts_long_name"], route_items["tts_short_name"], route_items["sorting_key"], None, route_items["real_time_route_id"]))
        return r_items                 
    
    class NotAFloatException(Exception):
        def __init__(self, value, message="Invalid Float Value! You passed {} which is of type {}! You need to pass a string(__str__)!"):
            self.value = value
            self.message = message.format(value, type(value))
            super().__init__(self.message)
    
        
    class NotAnIntException(Exception):
        def __init__(self, value, message="Invalid Int Value! You passed {} which is of type {}! You need to pass a string(__str__)!"):
            self.value = value
            self.message = message.format(value, type(value))
            super().__init__(self.message)    
        
    class NotABoolException(Exception):
        def __init__(self, value, message="Invalid Bool Value! You passed {} which is of type {}! You need to pass a bool(__bool__)!"):
            self.value = value
            self.message = message.format(value, type(value))
            super().__init__(self.message)
            
    
    class NotAStringException(Exception):
        def __init__(self, value, message="Invalid String Value! You passed {} which is of type {}! You need to pass a string(__str__)!"):
            self.value = value
            self.message = message.format(value, type(value))
            super().__init__(self.message)
    
    class SearchQueryResults:
        def __init__(self, global_stop_id, location_type, match_strength, parent_station_global_stop_id, route_type, stop_lat, stop_lon, stop_name):
            self.global_stop_id = global_stop_id
            self.location_type = location_type
            self.match_strength = match_strength
            self.parent_station_global_stop_id = parent_station_global_stop_id
            self.route_type = route_type
            self.stop_lat = stop_lat
            self.stop_lon = stop_lon
            self.stop_name = stop_name
        def return_global_stop_id(self):
            return self.global_stop_id
        def return_location_type(self):
            return self.location_type
        def return_match_strength(self):
            return self.match_strength
        def return_parent_station_global_stop_id(self):
            return self.parent_station_global_stop_id
        def return_route_type(self):
            return self.route_type
        def return_stop_lat(self):
            return self.stop_lat
        def return_stop_lon(self):
            return self.stop_lon
        def return_stop_name(self):
            return self.stop_name
        
    
    class Stop:
        def __init__(self, distance, global_stop_id, location_type, parent_station_global_stop, route_type, stop_lat, stop_lon, stop_name, stop_code, rt_stop_id, wheelchair_boarding):
            self.distance = distance
            self.global_stop_id = global_stop_id
            self.location_type = location_type
            self.parent_station_global_stop = parent_station_global_stop
            self.route_type = route_type
            self.stop_lat = stop_lat
            self.stop_lon = stop_lon
            self.stop_name = stop_name
            self.stop_code = stop_code
            self.rt_stop_id = rt_stop_id
            self.wheelchair_boarding = wheelchair_boarding
        def return_distance(self):
            return self.distance
        def return_global_stop_id(self):
            return self.global_stop_id
        def return_location_type(self):
            return self.location_type
        def return_parent_station_global_stop(self):
            return self.parent_station_global_stop
        def return_route_type(self):
            return self.route_type
        def return_stop_lattitude(self):
            return self.stop_lat
        def return_stop_longitude(self):
            return self.stop_lon
        def return_stop_name(self):
            return self.stop_name
        def return_stop_code(self):
            return self.stop_code
        def return_route_stop_id(self):
            return self.rt_stop_id
        def return_wheelchair_boarding(self):
            return self.wheelchair_boarding
            
    class ScheduleItem:
        def __init__(self, departure_time: int, is_cancelled: bool, is_real_time: bool, rt_trip_id: str, scheduled_departure_time: int, wheelchair_accessible: int, trip_search_key: str) -> None:
            self.departure_time = departure_time
            self.is_cancelled = is_cancelled
            self.is_real_time = is_real_time
            self.rt_trip_id = rt_trip_id
            self.scheduled_departure_time = scheduled_departure_time
            self.wheelchair_accessible = wheelchair_accessible
            self.trip_search_key = trip_search_key
        def get_departure_time(self):
            return self.departure_time
        def get_cancelled(self):
            return self.is_cancelled
        def get_is_real_time(self):
            return self.is_real_time
        def get_route_trip_id(self):
            return self.rt_trip_id
        def get_scheduled_departure_time(self):
            return self.scheduled_departure_time
        def get_wheelchair_accessibility(self):
            return self.wheelchair_accessible
        def get_trip_search_key(self):
            return self.trip_search_key
    
    class TruncatedScheduleItem:
        def __init__(self, departure, stop):
            self.departure = departure
            self.stop = stop
        def return_departure_time(self):
            return self.departure
        def return_stop_obj(self):
            return self.stop
        
        
        
    class TripPlan:
        def __init__(self, arriveBy, date, time, mode, fromPlace, numItineraries, toPlace, locale, walkReluctance, wheelchair, ignoreRealTimeUpdates, allowedNetworks) -> None:
            self.arrive_by = arriveBy
            self.date = date
            self.time = time
            self.mode = mode
            self.from_place = fromPlace
            self.num_itineraries = numItineraries
            self.to_place = toPlace
            self.locale = locale
            self.walk_reluctance = walkReluctance
            self.wheelchair = wheelchair
            self.ignore_real_time_updates = ignoreRealTimeUpdates
            self.allowed_networks = allowedNetworks
        def get_arrive_by(self):
            return self.arrive_by
        def get_date_tripplan(self):
            return self.date
        def get_time_tripplan(self):
            return self.time
        def get_mode_tripplan(self):
            return self.mode
        def get_from_place(self):
            return self.from_place
        def get_num_itineraries(self):
            return self.num_itineraries
        def get_to_place(self):
            return self.to_place
        def get_locale(self):
            return self.locale
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
                    
    class ToAndFrom_Loc:
        def __init__(self, lat, lon, name, vertex) -> None:
            self.lat = lat
            self.lon = lon
            self.name = name
            self.vertex_type = vertex
        def get_lat(self):
            return self.lat
        def get_lon(self):
            return self.lon
        def get_name(self):
            return self.name
        def get_vertex_type(self):
            self.vertex_type
    class MinimumTimes:
        def __init__(self, from_feed_id, from_stop_id, min_time, to_feed_id, to_stop_id) -> None:
            self.from_feed_id = from_feed_id
            self.from_stop_id = from_stop_id
            self.min_time = min_time
            self.to_feed_id = to_feed_id
            self.to_stop_id = to_stop_id
        def get_from_feed_id(self):
            return self.from_feed_id
        def get_from_stop_id(self):
            return self.from_stop_id
        def get_min_time(self):
            return self.min_time
        def get_to_feed_id(self):
            return self.to_feed_id
        def get_to_stop_id(self):
            return self.to_stop_id
        
    

    
    
    class Transfers:
        def __init__(self, buffer_time, default_minimum_times, minimum_times) -> None:
            self.buffer_time = buffer_time
            self.default_minimum_times = default_minimum_times
            self.minimum_times = minimum_times
        def get_buffer_time(self):
            return self.buffer_time
        def get_default_min_times(self):
            return self.default_minimum_times
        def get_min_times(self):
            return self.minimum_times
            
            
    
    
    
    class Plan:
        def __init__(self, date, from_loc, itineraries, to_loc) -> None:
            self.date = date
            self.from_loc = from_loc
            self.itineraries = itineraries
            self.to_loc = to_loc
        def get_date(self):
            return self.date
        def get_from_loc(self):
            return self.from_loc
        def get_itineraries(self):
            return self.itineraries
        def get_to_loc(self):
            return self.to_loc
    
    
    
    class CalculatedTripPlan:
        def __init__(self, plan, transfers) -> None:
            self.plan = plan
            self.transfers = transfers
        def get_plan(self):
            return self.plan
        def get_transfers(self):
            return self.transfers
    class Networks:
        def __init__(self, network_geometry, network_id, network_name, network_location) -> None:
            self.network_geometry = network_geometry
            self.network_id = network_id
            self.network_name = network_name
            self.network_location = network_location
        def get_network_geometry(self):
            return self.network_geometry
        def get_network_id(self):
            return self.network_id
        def get_network_name(self):
            return self.network_name
        def get_network_location(self):
            return self.network_location
    class ItineraryDetail:
        def __init__(self, direction_headsign, direction_id, headsign, merged_headsign, shape, stops, next_departure, canonical_itinerary, is_active) -> None:
            self.direction_headsign = direction_headsign
            self.direction_id = direction_id
            self.headsign = headsign
            self.merged_headsign = merged_headsign
            self.shape = shape
            self.stops = stops
            self.next_departure = next_departure
            self.canonical_itinerary = canonical_itinerary
            self.is_active = is_active
        def get_direction_headsign(self):
            return self.direction_headsign
        def get_direction_id(self):
            return self.direction_id
        def get_headsign(self):
            return self.headsign
        def get_merged_headsign(self):
            return self.merged_headsign
        def get_shape(self):
            return self.shape
        def get_stops(self):
            return self.stops
        def get_next_departure(self):
            return self.next_departure
        def get_canonical_itinerary(self):
            return self.canonical_itinerary
        def get_is_active(self):
            return self.is_active
            
    class DetailedRoute:
        def __init__(self, itineraries, route) -> None:
            self.itineraries = itineraries
            self.route = route
        def get_itineraries(self):
            return self.itineraries
        def get_route(self):
            return self.route
            
            
    
    class Itinerary:
        
        def __init__(self, direction_id: int, headsign: str, direction_headsign: str, merged_headsign: str, schedule_items: list, branch_code: str) -> None:
            self.direction_id = direction_id
            self.headsign = headsign
            self.direction_headsign = direction_headsign
            self.merged_headsign = merged_headsign
            self.schedule_items = schedule_items
            self.branch_code = branch_code
        def get_direction_id(self):
            return self.direction_id
        def get_direction_headsign(self):
            return self.direction_headsign
        def get_merged_headsign(self):
            return self.merged_headsign
        def get_schedule_items(self):
            return self.schedule_items
        def get_headsign(self):
            return self.headsign
        def get_branch_code(self):
            return self.branch_code
            
    class GivenNetwork:
        def __init__(self, network_id, lat, lon) -> None:
            self.network_id = network_id
            self.lat = lat
            self.lon = lon
        def get_network_id(self):
            return self.network_id
        def get_lat(self):
            return self.lat
        def get_lon(self):
            return self.lon
            
    class QueryStops:
        """_The Query Stops Object_
        
        
        """
        def __init__(self, lat: float, lon: float, query: str, pickup_dropoff_filter:str, max_num_results: int) -> None:
            """_Initialiser for the Query Stops object_

            Args:
                lat (float): _Latitude of the approximate area of the search._
                lon (float): _Longitude of the approximate area of the search._
                query (str): _Search term. Will be matched against the stop_name and stop_code of potential stops from the GTFS._
                pickup_dropoff_filter (str): _Enum: "PickupAllowedOnly" "DropoffAllowedOnly" "Everything" For routable stops, futher filter based on whether a rider can embark or disembark at this stop._
                max_num_results (int): _Maximum number of results to return. If there are few matches, less results than requested will be returned._
            """
            self.lat = lat
            self.lon = lon
            self.query = query
            self.pickup_dropoff_filter = pickup_dropoff_filter
            self.max_num_results = max_num_results
        def get_lat(self):
            """_Query: Get Latitude value of PyTransit instance_

            Returns:
                _float_: _The Latitude used for this PyTransit instance, as a float._
            """
            return self.lat
        def get_lon(self):
            """_Query: Gets the Longitude value of the PyTransit instance._

            Returns:
                _float_: _The Longitude used for this PyTransit instance, as a float._
            """
            return self.lon
        def get_query(self):
            """_summary_

            Returns:
                _str_: _The search term passed into the initialiser_
            """
            return self.query
        def get_pickup_dropoff_filter(self):
            """_Query: Gets the pickup-dropoff filter string from the Query Stop instance within PyTransit_

            Returns:
                _str_: _The drop off filter string_
            """
            return self.pickup_dropoff_filter
        def get_max_num_results(self):
            """_Query: Gets the max-num results int from the Query Stop instance within PyTransit_

            Returns:
                _int_: _The max-num results as an int_
            """
            return self.max_num_results
        
    class QueryStopResults:
        """_The Query Stop Results object, this is returned when you query a stop._
        """
        def __init__(self, global_stop_id, location_type, match_strength, parent_station_global_stop_id, route_type, stop_lat, stop_lon, stop_name) -> None:
            self.global_stop_id = global_stop_id
            self.location_type = location_type
            self.match_strength = match_strength
            self.parent_station_global_stop_id = parent_station_global_stop_id
            self.route_type = route_type
            self.stop_lat = stop_lat
            self.stop_lon = stop_lon
            self.stop_name = stop_name
        def get_global_stop_id(self):
            return self.global_stop_id
        def get_location_type(self):
            return self.location_type
        def get_match_strength(self):
            return self.match_strength
        def get_parent_station_global_id(self):
            return self.parent_station_global_stop_id
        def get_route_type(self):
            return self.route_type
        def get_stop_lat(self):
            return self.stop_lat
        def get_stop_lon(self):
            return self.stop_lon
        def get_stop_name(self):
            return self.stop_name
    class TripDetails:
        def __init__(self, route, rt_trip_id, schedule_items) -> None:
            self.route = route
            self.rt_trip_id = rt_trip_id
            self.schedule_items = schedule_items
        def get_route(self):
            return self.route
        def get_rt_trip_id(self):
            return self.rt_trip_id
        def get_schedule_items(self):
            return self.schedule_items
    class ScheduleForStop:
        def __init__(self, departure_time, stop) -> None:
            self.departure_time = departure_time
            self.stop = stop
        def get_departure_time(self):
            return self.departure_time
        def get_stop(self):
            return self.stop
    class PlanTripItinerary:
        def __init__(self, accessibility, duration, endTime, legs, startTime, transfers, transitTime, walkTime, wheelchairNeed) -> None:
            self.accessibility = accessibility
            self.duration = duration
            self.endTime = endTime
            self.legs = legs
            self.startTime = startTime
            self.transfers = transfers
            self.transitTime = transitTime
            self.walkTime = walkTime
            self.wheelchairNeed = wheelchairNeed
    class LegGeometry:
        def __init__(self, length, points) -> None:
            self.length = length
            self.points = points
            
    class ToFromNetwork:
        def __init__(self, ToFromObj, stopCode, stopId, globalStopId, stopIndex) -> None:
            self.tofrom_obj = ToFromObj
            self.stop_code = stopCode
            self.stop_id = stopId
            self.global_stop_id = globalStopId
            self.stop_index = stopIndex
    
    class Networks:
        def __init__(self, network_geometry, network_id, network_name, network_location):
            self.network_geometry = network_geometry
            self.network_id = network_id
            self.network_name = network_name
            self.network_location = network_location
        def get_network_geometry(self):
            return self.network_geometry
        def get_network_id(self):
            return self.network_id
        def get_network_name(self):
            return self.network_name
        def get_network_location(self):
            return self.network_location
        
            
    class legs:
        def __init__(self, agencyId, agencyName, agencyTimeZoneOffset, agencyUrl, distance, duration, endTime, from_ext, headsign, intermediateStops, legGeometry, mode, route, route_colour, routeId, globalRouteId, routeLongName, route_short_name, route_text_color, route_type, start_time, to_ext, transit_leg, trip_block_id, trip_id, trip_short_name, trip_search_key, interline_with_previous_leg, real_time, departure_delay, arrival_delay)  -> None:
            self.agency_id = agencyId
            self.agency_name = agencyName
            self.agency_timezone_offset = agencyTimeZoneOffset
            self.agency_url = agencyUrl
            self.distance = distance
            self.duration = duration
            self.end_time = endTime
            self.from_ext = from_ext
            self.headsign = headsign
            self.intermediate_stops = intermediateStops
            self.legGeometry = legGeometry
            self.mode = mode
            self.route = route
            self.route_colour = route_colour
            self.route_id = routeId
            self.global_route_id = globalRouteId
            self.route_short_name = route_short_name
            self.route_text_colour = route_text_color
            self.route_type = route_type
            self.start_time = start_time
            self.to_ext = to_ext
            self.transit_leg = transit_leg
            self.trip_block_id = trip_block_id
            self.trip_id = trip_id
            self.trip_short_name = trip_short_name
            self.trip_search_key = trip_search_key
            
    
            
            
            
        
            
            
    
    
    class Route:
        def __init__(self, global_route_id: str, itineraries, route_long_name: str, route_short_name: str, route_type: int, route_color: str, route_text_color: str, route_network_name: str, route_network_id: str, tts_long_name: str, tts_short_name: str, sorting_key: str, mode_name: str, real_time_route_id: str) -> None:
            self.global_route_id = global_route_id
            self.itineraries = itineraries
            self.route_long_name = route_long_name
            self.route_short_name = route_short_name
            self.route_type = route_type
            self.route_color = route_color
            self.route_text_color = route_text_color
            self.route_network_name = route_network_name
            self.route_network_id = route_network_id
            self.tts_long_name = tts_long_name
            self.tts_short_name = tts_short_name
            self.sorting_key = sorting_key
            self.mode_name = mode_name
            self.real_time_route_id = real_time_route_id
        def get_global_route_id(self):
            return self.global_route_id
        def get_itineraries(self):
            return self.itineraries
        def get_route_long_name(self):
            return self.route_long_name
        def get_route_short_name(self):
            return self.route_short_name
        def get_route_type(self):
            return self.route_type
        def get_route_color(self):
            return self.route_color
        def get_route_text_color(self):
            return self.route_text_color
        def get_route_network_name(self):
            return self.route_network_name
        def get_route_network_id(self):
            return self.route_network_id
        def get_tts_long_name(self):
            return self.tts_long_name
        def get_tts_short_name(self):
            return self.tts_short_name
        def get_sorting_key(self):
            return self.sorting_key
        def get_mode_name(self):
            return self.mode_name
        def get_real_time_route_id(self):
            return self.real_time_route_id
            
    class StopFilter(Enum):
        ROUTABLE = "Routable"
        ENTRANCEANDSTOPSOUTSIDE = "EntrancesAndStopsOutsideStations"
        ENTRANCES = "Entrances"
        ANY = "Any"
        
    class WheelchairAccessible(Enum):
        INHERIT = 0
        YES = 1
        NO = 2
        
        
    class PickupDropoffFilter(Enum):
        PickupOnly = "PickupAllowedOnly"
        DropoffOnly = "DropoffAllowedOnly"
        Everything = "Everything"
        
    class ModeType(Enum):
        BUS = 3
        
    class UpcomingDepartures:
        def __init__(self, global_stop_id, time, remove_cancelled: bool, should_update_realtime: bool):
            self.global_stop_id = global_stop_id
            self.time = time
            self.remove_cancelled = remove_cancelled
            self.should_update_realtime = should_update_realtime
        def get_global_stop_id(self):
            return self.global_stop_id
        def get_time(self):
            return self.time
        def get_remove_cancelled(self):
            return self.remove_cancelled
        def get_should_update_realtime(self):
            return self.should_update_realtime
    
        
    
    def __init__(self, lat = None, lon = None, distance=150, stop_filter=StopFilter.ROUTABLE, pick_drop_filter=None ):
        self.lat = lat
        self.lon = lon
        self.distance = distance
        self.stop_filter = stop_filter
        self.pick_drop_filter = pick_drop_filter
        self.stop_objs = []
        try:
            with open('.//api//apiKey.txt', 'r') as file:
                self.APIKEY = file.read().rstrip()
        except:
            print("Error Reading File!")
        
    
    def grabStopsByLatLon(self) -> list: 
        url = "https://external.transitapp.com/v3/public/nearby_stops"
        head = {"apiKey" : self.APIKEY}
        response = None
        resp_json = None
        p = {"lat" : self.lat, "lon" : self.lon, "max_distance" : self.distance, "stop_filter" : self.stop_filter}
        if self.pick_drop_filter is not None:
            p["pickup_dropoff_filter"] = self.pick_drop_filter
        try:
            response = requests.get(url=url,params=p,headers=head)
            resp_json = response.json()
            
        except requests.ConnectionError as con:
            print("Connection Error Raised! " + con.args)
        except requests.HTTPError as ht:
            print("HTTP Error! " + ht.args)
        except requests.Timeout as tm:
            print("A timeout occured: " + tm.args)
        print(response)
        if response is not None and response.status_code != 400:
            for x in resp_json['stops']:
                self.stop_objs.append(self.Stop(x['distance'], x['global_stop_id'], x['location_type'], x['parent_station_global_stop_id'], x['route_type'], x['stop_lat'], x['stop_lon'], x['stop_name'], x['stop_code'], x['rt_stop_id'], x['wheelchair_boarding']))
            print(x)
    
    
    def grabUpcomingDepartures(self, global_stop_id, time, remove_cancelled, should_update_realtime) -> list:
        url = "https://external.transitapp.com/v3/public/stop_departures"
        head = {"apiKey" : self.APIKEY}
        response = None
        resp_json = None
        obj_pool = []
        p = {"global_stop_id" : global_stop_id, "time" : time, "remove_cancelled" : remove_cancelled, "should_update_realtime" : should_update_realtime}
        try:
            response = requests.get(url=url,params=p,headers=head)
            resp_json = response.json()
        except requests.ConnectionError as con:
            print("Connection Error Raised! " + con.args)
        except requests.HTTPError as ht:
            print("HTTP Error! " + ht.args)
        except requests.Timeout as tm:
            print("A timeout occured: " + tm.args)
        print(response)
        if response is not None and response.status_code != 400:
            for x in resp_json["route_departures"]:
                obj_pool.append(self.Route(x['global_route_id'], (self.__constructListOfItineraries(x["itineraries"])), x['route_long_name'], x['route_short_name'], x['route_type'], x['route_color'], x['route_text_color'], x['route_network_name'], x['route_network_id'], x['tts_long_name'], x['tts_short_name'], x['sorting_key'], x['mode_name'], x['real_time_route_id']))
            return obj_pool
        
    def planTripFromOriginDestination(self, arriveBy, date, time, mode, fromPlace, numItineraries, toPlace, locale, walkReluctance, wheelchair, ignoreRealTimeUpdates, allowedNetworks):
        url = "https://external.transitapp.com/v3/otp/plan"
        head = {"apiKey" : self.APIKEY}
        response = None
        resp_json = None
        p = None
        plan_obj = None
        transfers_obj = None
        try:
            self.__checkBool(arriveBy)
            self.__checkBool(wheelchair)
            self.__checkBool(ignoreRealTimeUpdates)
            self.__checkString(date)
            self.__checkString(time)
            self.__checkString(mode)
            self.__checkString(fromPlace)
            self.__checkString(toPlace)
            self.__checkString(locale)
            self.__checkString(allowedNetworks)
            self.__checkInt(numItineraries)
            self.__checkFloat(walkReluctance)
        except (self.NotABoolException, self.NotAFloatException, self.NotAnIntException, self.NotAStringException) as e:
            print(e)
        try:
            p = {"arriveBy" : arriveBy, "date": date, "time" : time, "mode" : mode, "fromPlace" : fromPlace, "numItineraries" : numItineraries, "toPlace" : toPlace, "locale" : locale, "walkReluctance" : walkReluctance, "wheelchair" : wheelchair, "ignoreRealTimeUpdates" : ignoreRealTimeUpdates, "allowedNetworks" : allowedNetworks}
            response = requests.get(url=url, params=p, headers=head)
            resp_json = response.json()
            print(resp_json)
            if response is not None:
                plan_obj = self.Plan(resp_json["plan"]["date"], resp_json["plan"]["from"], [self.PlanTripItinerary(*pti) for pti in resp_json["plan"]["itineraries"]], resp_json["plan"]["to"])
                return plan_obj
        except requests.HTTPError as ht:
            print("HTTP Error! " + ht.args)
        except requests.ConnectionError as con:
            print("Connection Error! " + con.args)
        except requests.Timeout as tm:
            print("Timeout Error! " + tm.args)
        except JSONDecodeError as js:
            print("JSON Decoding Error! " + js.args)
            
    def getListOfAvaliableNetworks(self, include_all_networks, include_network_geometry):
        url = "https://external.transitapp.com/v3/public/available_networks"
        head = {"apiKey": self.APIKEY}
        response = None
        resp_json = None
        p = None
        net_obj = None
        try:
            self.__checkBool(value=include_all_networks)
            self.__checkBool(value=include_network_geometry)
        except (self.NotABoolException, self.NotAFloatException, self.NotAnIntException, self.NotAStringException) as e:
            print(e)
        try:
            p = {"lat": self.lat, "lon" : self.lon, "include_all_networks" : include_all_networks, "include_network_geometry" : include_network_geometry}
            response = requests.get(url=url, params=p, headers=head)
            resp_json = response.json()
            if response is not None:
                net_obj = []
                for n in resp_json["networks"]:
                    if not include_network_geometry:
                        net_obj.append(self.Networks(None, n["network_id"], n["network_name"], n["network_location"]))
                    else:
                        net_obj.append(self.Networks(n["network_geometry"], n["network_id"], n["network_name"], n["network_location"]))
                return net_obj
        except requests.HTTPError as ht:
            print("HTTP Error! " + ht.args)
        except requests.ConnectionError as con:
            print("Connection Error! " + con.args)
        except requests.Timeout as tm:
            print("Timeout Error! " + tm.args)
        except JSONDecodeError as js:
            print("JSON Decoding Error! " + js.args)
            
    def getDetailForRoute(self, global_route_id, include_next_departure):
        url = "https://external.transitapp.com/v3/public/route_details"
        head = {"apiKey": self.APIKEY}
        response = None
        resp_json = None
        p = None
        iti_obj = None
        rou_obj = None
        try:
            self.__checkString(global_route_id)
            self.__checkBool(include_next_departure)
        except (self.NotABoolException, self.NotAFloatException, self.NotAnIntException, self.NotAStringException) as e:
            print(e)
        try:
            p = {"global_route_id" : global_route_id, "include_next_departure" : include_next_departure}
            response = requests.get(url=url, params=p, headers=head)
            resp_json = response.json()
            print(resp_json["route"])
            if response is not None:
                iti_obj = []
                rou_obj = []
                print(resp_json["itineraries"])
                for i in resp_json["itineraries"]:
                    if not include_next_departure:
                        iti_obj.append(self.ItineraryDetail(i["direction_headsign"], i["direction_id"], i["headsign"], i["merged_headsign"], i["shape"], self.__constructListOfStops(i["stops"]), None, i["canonical_itinerary"], i["is_active"]))
                print(iti_obj)
                r = self.Route(global_route_id=resp_json["route"]["global_route_id"], route_long_name=resp_json["route"]["route_long_name"], route_short_name=resp_json["route"]["route_short_name"], route_type=resp_json["route"]["route_type"], route_color=resp_json["route"]["route_color"], route_text_color=resp_json["route"]["route_text_color"], route_network_name=resp_json["route"]["route_network_name"], route_network_id=resp_json["route"]["route_network_id"], tts_long_name=resp_json["route"]["tts_long_name"], tts_short_name=resp_json["route"]["tts_short_name"], sorting_key=resp_json["route"]["sorting_key"], mode_name=resp_json["route"]["mode_name"], real_time_route_id=resp_json["route"]["real_time_route_id"], itineraries=None)
                #r = self.Route(resp_json["route"]["global_route_id"],self.__constructListOfItineraries(resp_json["route"]["itineraries"]), resp_json["route"]["route_long_name"], resp_json["route"]["route_short_name"], resp_json["route"]["route_type"], resp_json["route"]["route_color"], resp_json["route"]["route_text_color"], resp_json["route"]["route_network_name"], resp_json["route"]["route_network_id"], resp_json["route"]["tts_long_name"], resp_json["route"]["tts_short_name"], resp_json["route"]["sorting_key"], resp_json["route"]["mode_name"], resp_json["route"]["real_time_route_id"])
                return {"itineraries" : iti_obj, "route" : r}
        except requests.HTTPError as ht:
            print("HTTP Error! " + ht.args)
        except requests.ConnectionError as con:
            print("Connection Error! " + con.args)
        except requests.Timeout as tm:
            print("Timeout Error! " + tm.args)
        except JSONDecodeError as js:
            print("JSON Decoding Error! " + js.args)
    
    def routesForAGivenNetwork(self, network_ids, include_itineraries):
        url = "https://external.transitapp.com/v3/public/routes_for_networks"
        head = {"apiKey": self.APIKEY}
        response = None
        resp_json = None
        p = None
        rou_obj = None
        try:
            self.__checkString(network_ids)
            self.__checkBool(include_itineraries)
        except (self.NotABoolException, self.NotAFloatException, self.NotAnIntException, self.NotAStringException) as e:
            print(e)
        try:
            p = {"network_ids" : network_ids, "lat" : self.lat, "lon" : self.lon, "include_itineraries" : include_itineraries}
            response = requests.get(url=url, params=p, headers=head)
            resp_json = response.json()
            rou_obj = []
            if not include_itineraries:
                for r in resp_json["routes"]:
                    rou_obj.append(self.Route(r["global_route_id"], None, r["route_long_name"], r["route_short_name"], r["route_type"], r["route_color"], r["route_text_color"], r["route_network_name"], r["route_network_id"], r["tts_long_name"], r["tts_short_name"], r["sorting_key"], r["mode_name"], r["real_time_route_id"]))
            else:
                for r in resp_json["routes"]:
                    rou_obj.append(self.Route(r["global_route_id"], self.__constructListOfItineraryDetails(r["itineraries"]), r["route_long_name"], r["route_short_name"], r["route_type"], r["route_color"], r["route_text_color"], r["route_network_name"], r["route_network_id"], r["tts_long_name"], r["tts_short_name"], r["sorting_key"], r["mode_name"], r["real_time_route_id"]))
            return rou_obj
        except requests.HTTPError as ht:
            print("HTTP Error! " + ht.args)
        except requests.ConnectionError as con:
            print("Connection Error! " + con.args)
        except requests.Timeout as tm:
            print("Timeout Error! " + tm.args)
        except JSONDecodeError as js:
            print("JSON Decoding Error! " + js.args)
    
    def stopsForAGivenNetwork(self, network_id):
        url = "https://external.transitapp.com/v3/public/stops_for_network"
        head = {"apiKey": self.APIKEY}
        response = None
        resp_json = None
        p = None
        stop_obj = None
        try:
            self.__checkString(network_id)
        except (self.NotABoolException, self.NotAFloatException, self.NotAnIntException, self.NotAStringException) as e:
            print(e)
        try:
            p = {"network_id" : network_id, "lat" : self.lat, "lon" : self.lon}
            response = requests.get(url=url, params=p, headers=head)
            resp_json = response.json()
            stop_obj = []
            stop_obj = self.__constructListOfStops(resp_json["stops"])
            return stop_obj
        except requests.HTTPError as ht:
            print("HTTP Error! " + ht.args)
        except requests.ConnectionError as con:
            print("Connection Error! " + con.args)
        except requests.Timeout as tm:
            print("Timeout Error! " + tm.args)
        except JSONDecodeError as js:
            print("JSON Decoding Error! " + js.args)    
    
    
    def latestUpdateForANetwork(self, network_id, to_date):
        url = "https://external.transitapp.com/v3/public/latest_update_for_network"
        head = {"apiKey": self.APIKEY}
        response = None
        resp_json = None
        p = None
        time_unix = None
        try:
            self.__checkString(network_id)
        except (self.NotABoolException, self.NotAFloatException, self.NotAnIntException, self.NotAStringException) as e:
            print(e)
        try:
            p = {"network_id" : network_id, "lat" : self.lat, "lon" : self.lon}
            response = requests.get(url=url, params=p, headers=head)
            resp_json = response.json()
            time_unix = resp_json["time"]
            if not to_date:
                return time_unix
            else:
                return datetime.datetime.fromtimestamp(time_unix)
        except requests.HTTPError as ht:
            print("HTTP Error! " + ht.args)
        except requests.ConnectionError as con:
            print("Connection Error! " + con.args)
        except requests.Timeout as tm:
            print("Timeout Error! " + tm.args)
        except JSONDecodeError as js:
            print("JSON Decoding Error! " + js.args)
    
    def findTransitStopsBySearchTerm(self, query, pickup_dropoff_filter, max_num_results):
        url = "https://external.transitapp.com/v3/public/search_stops"
        head = {"apiKey": self.APIKEY}
        response = None
        resp_json = None
        p = None
        result_obj = []
        try:
            self.__checkString(query)
            self.__checkString(pickup_dropoff_filter)
            self.__checkInt(max_num_results)
        except (self.NotABoolException, self.NotAFloatException, self.NotAnIntException, self.NotAStringException) as e:
            print(e)
        try:
            p = {"lat" : self.lat, "lon" : self.lon, "query" : query, "pickup_dropoff_filter" : pickup_dropoff_filter, "max_num_results" : max_num_results}
            response = requests.get(url=url, params=p, headers=head)
            resp_json = response.json()
            result_obj = self.__constructListOfSearchQueryResults(resp_json["results"])
            print(result_obj)
        except requests.HTTPError as ht:
            print("HTTP Error! " + ht.args)
        except requests.ConnectionError as con:
            print("Connection Error! " + con.args)
        except requests.Timeout as tm:
            print("Timeout Error! " + tm.args)
        except JSONDecodeError as js:
            print("JSON Decoding Error! " + js.args)
    
    
    def getDetailsForATrip(self, trip_search_key):
        url = "https://external.transitapp.com/v3/public/trip_details"
        head = {"apiKey": self.APIKEY}
        response = None
        resp_json = None
        p = None
        q = None
        trip_obj = None
        try:
            self.__checkString(trip_search_key)
        except (self.NotABoolException, self.NotAFloatException, self.NotAnIntException, self.NotAStringException) as e:
            print(e)
        try:
            p = {"trip_search_key" : trip_search_key}
            response = requests.get(url=url, params=p, headers=head)
            resp_json = response.json()
            if response.status_code == 404:
                raise requests.HTTPError("HTTP Status - 404" + "\n" + resp_json["message"])
            q = {"route": self.__constructCustomRoute(resp_json["route"]), "rt_trip_id" : resp_json["rt_trip_id"], "schedule_items" : self.__constructListOfTruncatedScheduleItems(resp_json["schedule_items"])}
            return q
            
                
        except requests.HTTPError as ht:
            print("HTTP Error! " + ht.args)
        except requests.ConnectionError as con:
            print("Connection Error! " + con.args)
        except requests.Timeout as tm:
            print("Timeout Error! " + tm.args)
        except JSONDecodeError as js:
            print("JSON Decoding Error! " + js.args)
    
    
    
    
    
    
    
    
    
    def grab_stops(self):
        return self.stop_objs

    
pool = None
test = TransitObj(43.605380, -79.645870, 150, "Routable", None)
time_val = int(time.time())
#test.grabStopsByLatLon()
pool = test.grabUpcomingDepartures('MIWAY:33113', time_val, True, False)

id = pool[0].get_itineraries()[0].get_schedule_items()[2].get_trip_search_key()

qp = test.getDetailsForATrip(id)
print(id)
#qp = test.getDetailForRoute(id, False)

#pool = test.routesForAGivenNetwork('MiWay|Mississauga', True)
#pool = test.stopsForAGivenNetwork(network_id="MiWay|Mississauga")
#pool = test.findTransitStopsBySearchTerm("Hurontario", "Everything", 35)
#print(qp["route"].get_route_short_name() + " - " + qp["route"].get_route_long_name() )



#print(pool[0].get_route_short_name() + "-", pool[0].get_route_long_name(), pool[0].get_route_type(), pool[0].get_route_network_name(), )

#print(isinstance(q, list))



