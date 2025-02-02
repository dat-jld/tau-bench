from tau_bench.envs.airline import tools
from tau_bench.annotation.code_exec import get_random, set_env, set_collection, get_data
from tau_bench.annotation.trajectory import set_function_names, set_tools
from tau_bench.envs.airline.tools.checks import set_annotation_mode
import json

set_annotation_mode(True)
set_env("airline")
set_collection(["reservations", "flights", "users"])
set_tools(tools)
set_function_names([
    'BookReservation',
    'Calculate',
    'CancelReservation',
    'GetReservationDetails',
    'GetUserDetails',
    'ListAllAirports',
    'SearchDirectFlight',
    'SearchOnestopFlight',
    'SendCertificate',
    'TransferToHumanAgents',
    'UpdateReservationBaggages',
    'UpdateReservationFlights',
    'UpdateReservationPassengers'
])

def get_random_reservation():
    reservation = get_random("reservations")
    user_id = reservation[1]["user_id"]
    print("Reservation:")
    print(json.dumps(reservation[1], indent=2))
    print("User:")
    print(json.dumps(json.loads(tools.GetUserDetails.invoke(get_data(), user_id)), indent=2))

def get_random_flight():
    print("Flight:")
    print(json.dumps(get_random("flights")[1], indent=2))
