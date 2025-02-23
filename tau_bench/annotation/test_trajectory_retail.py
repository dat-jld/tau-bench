import pytest
from .trajectory import replay, reset, get_functions
    
@pytest.fixture(autouse=True)
def run_around_tests():
    from . import retail
    reset()
    for key, func in get_functions().items():
        globals()[key] = func
    yield

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
    