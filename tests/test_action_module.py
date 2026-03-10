import unittest

from pybatgym.action.discrete import DiscreteActionMapper

class TestActionMappers(unittest.TestCase):
    def test_discrete_mapper(self):
        mapper = DiscreteActionMapper(max_queue_size=10)
        self.assertEqual(mapper.get_space().n, 11)
        
        mapper.reset()
        mapper.update_queue(["job_1", "job_2", "job_3"])
        
        # Valid execution
        events = mapper.map(1, 10.0)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["type"], "EXECUTE_JOB")
        self.assertEqual(events[0]["data"]["job_id"], "job_2")
        self.assertEqual(mapper.waiting_job_ids, ["job_1", "job_3"])
        
        # Invalid execution (out of bounds)
        events2 = mapper.map(5, 11.0)
        self.assertEqual(len(events2), 0) # No jobs executed

if __name__ == "__main__":
    unittest.main()
