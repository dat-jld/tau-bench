from tau_bench.envs.retail import tools
from code_exec import get_random, set_env, set_collection, get_random_user, get_data
from trajectory import replay, export, reset, set_function_names, set_tools, get_functions, _export_api
import json

set_env("retail")
set_collection(["orders", "products", "users"])
set_tools(tools)
set_function_names([
    'Calculate',
    'CancelPendingOrder',
    'ExchangeDeliveredOrderItems',
    'FindUserIdByEmail',
    'FindUserIdByNameZip',
    'GetOrderDetails',
    'GetProductDetails',
    'GetUserDetails',
    'ListAllProductTypes',
    'ModifyPendingOrderAddress',
    'ModifyPendingOrderItems',
    'ModifyPendingOrderPayment',
    'ModifyUserAddress',
    'ReturnDeliveredOrderItems',
    'TransferToHumanAgents'
])

def get_random_order():
    """
    Get a random order from the database and the corresponding user data as a starting point
    """
    order = get_random("orders")
    user_id = order[1]["user_id"]
    print("Order:")
    print(json.dumps(order[1], indent=2))
    print("User:")
    print(json.dumps(json.loads(tools.GetUserDetails.invoke(get_data(), user_id)), indent=2))

reset()

for key, func in get_functions().items():
    globals()[key] = func

# Example:
# cancel_pending_order(order_id="#W4184032", reason="no longer needed")
