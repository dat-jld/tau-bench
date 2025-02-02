# Copyright Sierra

from typing import Any, Dict
from tau_bench.envs.airline.tools.checks import is_annotation_mode, get_reservation_flight_status
from tau_bench.envs.tool import Tool


class SendCertificate(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        amount: int,
    ) -> str:
        users = data["users"]
        if user_id not in users:
            return "Error: user not found"
        user = users[user_id]
        
        if is_annotation_mode():
            premium_membership = user["membership"] != "regular"
            def prereqs(reservation):
                return premium_membership or reservation["cabin"] == "business" or reservation["insurance"] == "yes"
            reservations = [data["reservations"][reservation_id] for reservation_id in user["reservations"]]
            reservations_with_cancellations = [reservation for reservation in reservations if prereqs(reservation) and any(get_reservation_flight_status(data, flight) == "cancelled" for flight in reservation["flights"])]
            reservations_with_delays = [reservation for reservation in reservations if prereqs(reservation) and any(get_reservation_flight_status(data, flight) == "delayed" for flight in reservation["flights"])]
            allowed_amounts = [len(reservation["passengers"]) * 100 for reservation in reservations_with_cancellations] + [len(reservation["passengers"]) * 50 for reservation in reservations_with_delays]
            if len(allowed_amounts) == 0:
                return "AnnotationError: user has no reservation with a cancelled or delayed flight"
            if amount not in allowed_amounts:
                return "AnnotationError: user has no reservation eligible for that amount"

        # add a certificate, assume at most 3 cases per task
        for id in [3221322, 3221323, 3221324]:
            payment_id = f"certificate_{id}"
            if payment_id not in user["payment_methods"]:
                user["payment_methods"][payment_id] = {
                    "source": "certificate",
                    "amount": amount,
                    "id": payment_id,
                }
                return f"Certificate {payment_id} added to user {user_id} with amount {amount}."

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_certificate",
                "description": "Send a certificate to a user. Be careful!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user to book the reservation, such as 'sara_doe_496'.",
                        },
                        "amount": {
                            "type": "number",
                            "description": "Certificate amount to send.",
                        },
                    },
                    "required": ["user_id", "amount"],
                },
            },
        }
