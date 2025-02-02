ANNOTATION_MODE = False

def set_annotation_mode(value):
    global ANNOTATION_MODE
    ANNOTATION_MODE = value
    
def is_annotation_mode():
    return ANNOTATION_MODE

bag_allowance_table = {
    ("regular", "basic_economy"): 0,
    ("regular", "economy"): 1,
    ("regular", "business"): 2,
    ("silver", "basic_economy"): 1,
    ("silver", "economy"): 2,
    ("silver", "business"): 3,
    ("gold", "basic_economy"): 2,
    ("gold", "economy"): 3,
    ("gold", "business"): 3,
}

def check_bag_allowance(user, reservation):
    total_baggages = reservation["total_baggages"]
    nonfree_baggages = reservation["nonfree_baggages"]
    if total_baggages < 0 or nonfree_baggages < 0:
        return "AnnotationError: baggages arguments must be non-negative"
    free_baggages = total_baggages - nonfree_baggages
    if free_baggages < 0:
        return "AnnotationError: total_baggages cannot be less than nonfree_baggages"
    allowed_free_baggages = len(reservation["passengers"]) * bag_allowance_table[(user["membership"], reservation["cabin"])]
    if free_baggages > allowed_free_baggages:
        return "AnnotationError: too many free baggages"
    if total_baggages <= allowed_free_baggages and nonfree_baggages > 0:
        return "AnnotationError: free baggage allowance not fully used"
    return None

def get_reservation_flight(data, flight):
    flights = data["flights"]
    return flights[flight["flight_number"]]["dates"][flight["date"]]

def get_reservation_flight_status(data, flight):
    return get_reservation_flight(data, flight)["status"]

def get_reservation_flights(data, reservation_id):
    reservation = data["reservations"][reservation_id]
    return [get_reservation_flight(data, flight) for flight in reservation["flights"]]