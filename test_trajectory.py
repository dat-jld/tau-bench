from tau_bench.envs.retail import tools
from code_exec import set_env, set_collection
from trajectory import replay, reset, set_function_names, set_tools, get_functions

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

reset()

for key, func in get_functions().items():
    globals()[key] = func

def test_error():
    assert find_user_id_by_email(email="foo") == 'Error: user not found'

def test_replay_1():
    replay(
        [
            {
                "name": "find_user_id_by_name_zip",
                "arguments": {
                "first_name": "Mei",
                "last_name": "Davis",
                "zip": "80217"
                }
            },
            {
                "name": "get_user_details",
                "arguments": {
                "user_id": "mei_davis_8935"
                }
            },
            {
                "name": "get_order_details",
                "arguments": {
                "order_id": "#W2890441"
                }
            },
            {
                "name": "get_order_details",
                "arguments": {
                "order_id": "#W1267569"
                }
            },
            {
                "name": "get_product_details",
                "arguments": {
                "product_id": "2747247837"
                }
            },
            {
                "name": "get_product_details",
                "arguments": {
                "product_id": "4794339885"
                }
            },
            {
                "name": "return_delivered_order_items",
                "arguments": {
                "order_id": "#W2890441",
                "item_ids": ["2366567022"],
                "payment_method_id": "credit_card_1061405"
                }
            }
        ]
    )
    assert get_order_details(order_id="#W2890441")["status"] == "return requested"
    