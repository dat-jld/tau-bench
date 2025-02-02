# Copyright Sierra

import json
from typing import Any, Dict
from tau_bench.envs.airline.tools.checks import is_annotation_mode, get_reservation_flight_status
from tau_bench.envs.tool import Tool


class CancelReservation(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
    ) -> str:
        reservations = data["reservations"]
        if reservation_id not in reservations:
            return "Error: reservation not found"
        reservation = reservations[reservation_id]

        if is_annotation_mode():
            if (reservation["cabin"] != "business"
                and reservation["created_at"] < "2024-05-14T15:00:00"
                and not any(get_reservation_flight_status(data, flight) == "cancelled" for flight in reservation["flights"])
                and reservation["insurance"] == "no"):
                return "AnnotationError: flight cannot be cancelled (user/reservation not eligible)"
            if any(get_reservation_flight_status(data, flight) in ["flying", "landed"] for flight in reservation["flights"]):
                return "AnnotationError: flight cannot be cancelled (flights already used)"

        # reverse the payment
        refunds = []
        for payment in reservation["payment_history"]:
            refunds.append(
                {
                    "payment_id": payment["payment_id"],
                    "amount": -payment["amount"],
                }
            )
        reservation["payment_history"].extend(refunds)
        reservation["status"] = "cancelled"
        return json.dumps(reservation)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_reservation",
                "description": "Cancel the whole reservation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation ID, such as 'ZFA04Y'.",
                        },
                    },
                    "required": ["reservation_id"],
                },
            },
        }
