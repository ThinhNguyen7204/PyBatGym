import unittest
import numpy as np

from pybatgym.observation.simple import SimpleObservationBuilder
from pybatgym.batsim.events import EventType, JobSubmittedEvent, JobCompletedEvent

class TestObservationbuilders(unittest.TestCase):
    def test_simple_observation(self):
        builder = SimpleObservationBuilder()
        builder.reset()
        
        # Initial Space
        obs = builder.get_observation()
        self.assertTrue(np.array_equal(obs, np.array([0, 0, 0], dtype=np.float32)))
        self.assertEqual(builder.get_space().shape, (3,))
        
        # Job submitted
        event_submit = JobSubmittedEvent(timestamp=1.0, type=EventType.JOB_SUBMITTED, data={}, job_id="job1", job_profile={})
        builder.update(event_submit)
        
        obs = builder.get_observation()
        self.assertTrue(np.array_equal(obs, np.array([1, 0, 0], dtype=np.float32)))
        
        # Job started
        builder.notify_job_started()
        obs = builder.get_observation()
        self.assertTrue(np.array_equal(obs, np.array([0, 1, 0], dtype=np.float32)))
        
        # Job completed
        event_completed = JobCompletedEvent(timestamp=10.0, type=EventType.JOB_COMPLETED, data={}, job_id="job1", job_state="COMPLETED", return_code=0, alloc="0")
        builder.update(event_completed)
        obs = builder.get_observation()
        self.assertTrue(np.array_equal(obs, np.array([0, 0, 1], dtype=np.float32)))

if __name__ == "__main__":
    unittest.main()
