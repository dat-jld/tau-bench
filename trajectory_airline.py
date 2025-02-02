from tau_bench.annotation.code_exec import get_random_user, get_data
from tau_bench.annotation.trajectory import replay, export, reset, get_functions, _export_api
from tau_bench.annotation.airline import get_random_flight, get_random_reservation
from tau_bench.envs.airline.tools.checks import get_reservation_flights

reset()

for key, func in get_functions().items():
    globals()[key] = func

# Example:
# cancel_reservation(reservation_id="AQ12FI")