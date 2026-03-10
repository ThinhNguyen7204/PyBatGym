import unittest
from pybatgym.batsim.events import EventType, parse_event, JobSubmittedEvent
from pybatgym.batsim.protocol import BatSimProtocol

class TestBatSimIntegration(unittest.TestCase):
    def test_protocol_build_execute(self):
        msg = BatSimProtocol.build_execute_job(10.5, "job_1", "0-3")
        self.assertEqual(msg["type"], "EXECUTE_JOB")
        self.assertEqual(msg["timestamp"], 10.5)
        self.assertEqual(msg["data"]["job_id"], "job_1")
        self.assertEqual(msg["data"]["alloc"], "0-3")

    def test_parse_job_submitted(self):
        raw_msg = {
            "timestamp": 2.0,
            "type": "JOB_SUBMITTED",
            "data": {
                "job_id": "job_1",
                "job": {"res": 4, "walltime": 100}
            }
        }
        event = parse_event(raw_msg)
        self.assertIsInstance(event, JobSubmittedEvent)
        self.assertEqual(event.job_id, "job_1")
        self.assertEqual(event.job_profile["res"], 4)

    def test_parse_batsim_message(self):
        payload = {
            "now": 10.0,
            "events": [
                {"timestamp": 10.0, "type": "SIMULATION_BEGIN"}
            ]
        }
        now, events = BatSimProtocol.parse_message(payload)
        self.assertEqual(now, 10.0)
        self.assertEqual(len(events), 1)

if __name__ == "__main__":
    unittest.main()
