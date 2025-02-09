
from tau_bench.envs.retail import tools
from tau_bench.annotation.code_exec import get_random, set_env, set_collection, get_data
from tau_bench.annotation.trajectory import set_function_names, set_tools
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

def get_random_similar_orders():
    while True:
        user = get_random("users")[1]
        if len(user["orders"]) < 2:
            continue
        previous_orders_products_by_status = {"pending": set(), "delivered": set()}
        relevant_statuses = previous_orders_products_by_status.keys()
        ambiguous_product = None
        ambiguous_status = None
        orders = []
        for order_id in user["orders"]:
            order = json.loads(tools.GetOrderDetails.invoke(get_data(), order_id=order_id))
            orders.append(order)
            status = order["status"]
            product_set = set()
            if status not in relevant_statuses:
                continue
            for item in order["items"]:
                name = item["name"]
                if name in previous_orders_products_by_status[status]:
                    ambiguous_status = status
                    ambiguous_product = name
                    break
                else:
                    product_set.add(name)
            if (ambiguous_product):
                break
            previous_orders_products_by_status[status].update(product_set)
        if ambiguous_product:
            ambiguous_orders = [order for order in orders if order["status"] == ambiguous_status and any(item["name"] == ambiguous_product for item in order["items"])]
            print("Common item:", ambiguous_product)
            print("Order status:", ambiguous_status)
            print(len(ambiguous_orders), "orders:")
            print(json.dumps(ambiguous_orders, indent=2))
            print("User:")
            print(json.dumps(user, indent=2))
            break

