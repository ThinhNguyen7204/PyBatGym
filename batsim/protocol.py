from typing import List, Dict, Any

class BatSimProtocol:
    """Protocol encoder/decoder for communicating with BatSim via JSON."""

    @staticmethod
    def parse_message(message_json: dict) -> tuple[float, List[dict]]:
        """Parses a received BatSim message and returns the current time and events."""
        now = message_json.get("now", 0.0)
        events = message_json.get("events", [])
        return now, events

    @staticmethod
    def build_execute_job(timestamp: float, job_id: str, alloc: str) -> dict:
        return {
            "timestamp": timestamp,
            "type": "EXECUTE_JOB",
            "data": {
                "job_id": job_id,
                "alloc": alloc
            }
        }

    @staticmethod
    def build_reject_job(timestamp: float, job_id: str) -> dict:
        return {
            "timestamp": timestamp,
            "type": "REJECT_JOB",
            "data": {
                "job_id": job_id
            }
        }

    @staticmethod
    def build_call_me_later(timestamp: float, future_time: float) -> dict:
        return {
            "timestamp": timestamp,
            "type": "CALL_ME_LATER",
            "data": {"timestamp": future_time}
        }

    @staticmethod
    def build_reply(now: float, events: List[dict] = None) -> dict:
        """Wraps commands in the standard payload structure."""
        return {
            "now": now,
            "events": events or []
        }
