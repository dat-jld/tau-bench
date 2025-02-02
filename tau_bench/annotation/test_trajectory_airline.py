import json
import pytest

from tau_bench.envs.airline.tasks import tasks
from .trajectory import replay_to_string, reset, get_functions

@pytest.fixture(autouse=True)
def run_around_tests():
    from . import airline
    reset()
    for key, func in get_functions().items():
        globals()[key] = func
    yield
    
def assert_no_annotation_error(trajectory):
    assert "AnnotationError" not in trajectory
    
def assert_annotation_error(trajectory):
    assert "AnnotationError" in trajectory
    
def test_replay_all_tasks():
    has_error  = ["AnnotationError" in replay_to_string(task["actions"]) for task in tasks]
    errorCount = sum(has_error)
    for i in range(len(tasks)):
        if has_error[i]:
            task = tasks[i]
            # print(json.dumps(task, indent=2))
            print(task["instruction"])
            print(replay_to_string(task["actions"]))
    assert errorCount == 8

def test_replay_1():
    assert_no_annotation_error(replay_to_string(
        [
          {
            "name": "cancel_reservation",
            "kwargs": {
              "reservation_id": "Z7GOZK"
            }
          }
        ]
    ))

def test_replay_2():
    assert_no_annotation_error(replay_to_string(
        [
          {
            "name": "cancel_reservation",
            "kwargs": {
              "reservation_id": "K1NW8N"
            }
          },
          {
            "name": "book_reservation",
            "kwargs": {
              "user_id": "mohamed_silva_9265",
              "origin": "JFK",
              "destination": "SFO",
              "flight_type": "round_trip",
              "cabin": "business",
              "flights": [
                {
                  "flight_number": "HAT023",
                  "date": "2024-05-26"
                },
                {
                  "flight_number": "HAT204",
                  "date": "2024-05-28"
                },
                {
                  "flight_number": "HAT100",
                  "date": "2024-05-28"
                }
              ],
              "passengers": [
                {
                  "first_name": "Mohamed",
                  "last_name": "Silva",
                  "dob": "1960-11-26"
                },
                {
                  "first_name": "Raj",
                  "last_name": "Sanchez",
                  "dob": "1986-09-12"
                },
                {
                  "first_name": "Liam",
                  "last_name": "Wilson",
                  "dob": "1980-03-27"
                }
              ],
              "payment_methods": [
                {
                  "payment_id": "certificate_3765853",
                  "amount": 500
                },
                {
                  "payment_id": "gift_card_8020792",
                  "amount": 198
                },
                {
                  "payment_id": "gift_card_6136092",
                  "amount": 129
                },
                {
                  "payment_id": "credit_card_2198526",
                  "amount": 1786
                }
              ],
              "total_baggages": 0,
              "nonfree_baggages": 0,
              "insurance": "no"
            }
          }
        ]
    ))

def test_replay_3():
    assert_no_annotation_error(replay_to_string(
        [
            { "name": "cancel_reservation", "arguments": { "reservation_id": "K1NW8N" } },
            {
                "name": "book_reservation",
                "arguments": {
                "user_id": "mohamed_silva_9265",
                "origin": "JFK",
                "destination": "SFO",
                "flight_type": "round_trip",
                "cabin": "business",
                "flights": [
                    { "flight_number": "HAT023", "date": "2024-05-26" },
                    { "flight_number": "HAT204", "date": "2024-05-28" },
                    { "flight_number": "HAT100", "date": "2024-05-28" }
                ],
                "passengers": [
                    {
                    "first_name": "Mohamed",
                    "last_name": "Silva",
                    "dob": "1960-11-26"
                    },
                    {
                    "first_name": "Raj",
                    "last_name": "Sanchez",
                    "dob": "1986-09-12"
                    },
                    {
                    "first_name": "Liam",
                    "last_name": "Wilson",
                    "dob": "1980-03-27"
                    }
                ],
                "payment_methods": [
                    { "payment_id": "certificate_3765853", "amount": 500 },
                    { "payment_id": "gift_card_8020792", "amount": 198 },
                    { "payment_id": "gift_card_6136092", "amount": 129 },
                    { "payment_id": "credit_card_2198526", "amount": 1786 }
                ],
                "total_baggages": 0,
                "nonfree_baggages": 0,
                "insurance": "no"
                }
            }
        ]
    ))
    
def test_replay_4():
    assert_no_annotation_error(replay_to_string(
        [
            {
                "name": "update_reservation_flights",
                "arguments": {
                "reservation_id": "OBUT9V",
                "cabin": "economy",
                "flights": [
                    { "flight_number": "HAT078", "date": "2024-05-27" },
                    { "flight_number": "HAT118", "date": "2024-05-27" },
                    { "flight_number": "HAT290", "date": "2024-05-27" },
                    { "flight_number": "HAT175", "date": "2024-05-27" }
                ],
                "payment_id": "gift_card_6276644"
                }
            },
            {
                "name": "update_reservation_baggages",
                "arguments": {
                "reservation_id": "OBUT9V",
                "total_baggages": 2,
                "nonfree_baggages": 0,
                "payment_id": "gift_card_6276644"
                }
            }
        ]
    ))
    
def test_replay_5():
    assert_no_annotation_error(replay_to_string(
        [
          {
            "name": "update_reservation_flights",
            "kwargs": {
              "reservation_id": "JG7FMM",
              "cabin": "economy",
              "flights": [
                {
                  "flight_number": "HAT028",
                  "date": "2024-05-21"
                },
                {
                  "flight_number": "HAT277",
                  "date": "2024-05-21"
                }
              ],
              "payment_id": "credit_card_2929732"
            }
          },
          {
            "name": "update_reservation_flights",
            "kwargs": {
              "reservation_id": "2FBBAH",
              "cabin": "economy",
              "flights": [
                {
                  "flight_number": "HAT080",
                  "date": "2024-05-28"
                },
                {
                  "flight_number": "HAT076",
                  "date": "2024-05-28"
                },
                {
                  "flight_number": "HAT255",
                  "date": "2024-05-30"
                },
                {
                  "flight_number": "HAT148",
                  "date": "2024-05-30"
                }
              ],
              "payment_id": "gift_card_3481935"
            }
          },
          {
            "name": "update_reservation_flights",
            "kwargs": {
              "reservation_id": "X7BYG1",
              "cabin": "economy",
              "flights": [
                {
                  "flight_number": "HAT232",
                  "date": "2024-05-24"
                },
                {
                  "flight_number": "HAT228",
                  "date": "2024-05-24"
                }
              ],
              "payment_id": "credit_card_2929732"
            }
          },
          {
            "name": "update_reservation_flights",
            "kwargs": {
              "reservation_id": "EQ1G6C",
              "cabin": "economy",
              "flights": [
                {
                  "flight_number": "HAT084",
                  "date": "2024-05-23"
                },
                {
                  "flight_number": "HAT175",
                  "date": "2024-05-23"
                }
              ],
              "payment_id": "gift_card_6847880"
            }
          },
          {
            "name": "update_reservation_flights",
            "kwargs": {
              "reservation_id": "BOH180",
              "cabin": "economy",
              "flights": [
                {
                  "flight_number": "HAT276",
                  "date": "2024-05-21"
                },
                {
                  "flight_number": "HAT279",
                  "date": "2024-05-22"
                }
              ],
              "payment_id": "credit_card_9525117"
            }
          }
        ]
    ))
    
def test_replay_6():
    # Economy flights not cancellable
    assert_annotation_error(replay_to_string(
        [ 
            { 
                "name": "get_reservation_details", 
                "arguments": {"reservation_id": "XEHM4B"}, 
            }, 
            { 
                "name": "get_reservation_details", 
                "arguments": {"reservation_id": "59XX6W"}, 
            }, 
            {"name": "calculate", "arguments": {"expression": "(65 + 83) * 2"}}, 
            {"name": "calculate", "arguments": {"expression": "(168 + 114) * 2"}}, 
            { 
                "name": "update_reservation_flights", 
                "arguments": { 
                    "reservation_id": "XEHM4B", 
                    "cabin": "economy", 
                    "flights": [ 
                        {"flight_number": "HAT005", "date": "2024-05-20"}, 
                        {"flight_number": "HAT178", "date": "2024-05-30"}, 
                    ], 
                    "payment_id": "credit_card_2408938", 
                }, 
            }, 
            {"name": "cancel_reservation", "arguments": {"reservation_id": "XEHM4B"}}, 
            {"name": "cancel_reservation", "arguments": {"reservation_id": "59XX6W"}}, 
        ]
    ))
    
def test_replay_6b():
    # Business flights cancellable
    assert_no_annotation_error(replay_to_string(
        [ 
            { 
                "name": "get_reservation_details", 
                "arguments": {"reservation_id": "XEHM4B"}, 
            }, 
            { 
                "name": "get_reservation_details", 
                "arguments": {"reservation_id": "59XX6W"}, 
            },
            { 
                "name": "update_reservation_flights", 
                "arguments": { 
                    "reservation_id": "XEHM4B", 
                    "cabin": "business", 
                    "flights": [ 
                        {"flight_number": "HAT005", "date": "2024-05-20"}, 
                        {"flight_number": "HAT178", "date": "2024-05-30"}, 
                    ], 
                    "payment_id": "credit_card_2408938", 
                }, 
            }, 
            {"name": "cancel_reservation", "arguments": {"reservation_id": "XEHM4B"}}, 
        ]
    ))
    
def test_replay_7():
    # No delayed flights
    assert_annotation_error(replay_to_string(
        [
          {
            "name": "get_user_details",
            "kwargs": {
              "user_id": "noah_muller_9847"
            }
          },
          {
            "name": "get_reservation_details",
            "kwargs": {
              "reservation_id": "SDZQKO"
            }
          },
          {
            "name": "get_reservation_details",
            "kwargs": {
              "reservation_id": "4OG6T3"
            }
          },
          {
            "name": "send_certificate",
            "kwargs": {
              "user_id": "noah_muller_9847",
              "amount": 50
            }
          }
        ]
    ))
    
def test_replay_8():
    assert_no_annotation_error(replay_to_string(
        [
          {
            "name": "get_user_details",
            "kwargs": {
              "user_id": "ethan_martin_2396"
            }
          },
          {
            "name": "send_certificate",
            "kwargs": {
              "user_id": "ethan_martin_2396",
              "amount": 150
            }
          }
        ]
    ))
    
def test_replay_8b():
    # Wrong amount
    assert_annotation_error(replay_to_string(
        [
          {
            "name": "get_user_details",
            "kwargs": {
              "user_id": "ethan_martin_2396"
            }
          },
          {
            "name": "send_certificate",
            "kwargs": {
              "user_id": "ethan_martin_2396",
              "amount": 300
            }
          }
        ]
    ))

def test_replay_9():
    assert_annotation_error(replay_to_string(
        [
          {
            "name": "get_reservation_details",
            "kwargs": {
              "reservation_id": "VA5SGQ"
            }
          },
          {
            "name": "update_reservation_flights",
            "kwargs": {
              "reservation_id": "VA5SGQ",
              "cabin": "economy",
              "flights": [
                {
                  "flight_number": "HAT169",
                  "date": "2024-05-17"
                },
                {
                  "flight_number": "HAT033",
                  "date": "2024-05-19"
                }
              ],
              "payment_id": "credit_card_8003957"
            }
          },
          {
            "name": "update_reservation_baggages",
            "kwargs": {
              "reservation_id": "VA5SGQ",
              "total_baggages": 1,
              "nonfree_baggages": 1,
              "payment_id": "credit_card_8003957"
            }
          }
        ]
    ))
    
def test_replay_9b():
    # Invalid flights
    assert_annotation_error(replay_to_string(
        [
          {
            "name": "get_reservation_details",
            "kwargs": {
              "reservation_id": "VA5SGQ"
            }
          },
          {
            "name": "update_reservation_flights",
            "kwargs": {
              "reservation_id": "VA5SGQ",
              "cabin": "economy",
              "flights": [
                {
                  "flight_number": "HAT169",
                  "date": "2024-05-17"
                },
                {
                  "flight_number": "HAT033",
                  "date": "2024-05-19"
                }
              ],
              "payment_id": "credit_card_8003957"
            }
          },
          {
            "name": "update_reservation_baggages",
            "kwargs": {
              "reservation_id": "VA5SGQ",
              "total_baggages": 1,
              "nonfree_baggages": 1,
              "payment_id": "credit_card_8003957"
            }
          }
        ]
    ))