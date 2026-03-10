import unittest
from pybatgym.reward.metrics import SlowdownRewardCalculator, UtilizationRewardCalculator
from pybatgym.reward.multi import MultiObjectiveRewardCalculator
from pybatgym.batsim.events import EventType, JobCompletedEvent, JobSubmittedEvent

class TestRewardModule(unittest.TestCase):

    def test_slowdown_reward(self):
        calc = SlowdownRewardCalculator()
        
        event = JobCompletedEvent(
            timestamp=10.0,
            type=EventType.JOB_COMPLETED,
            data={"waiting_time": 10.0, "execution_time": 5.0},
            job_id="job_1",
            job_state="COMPLETED",
            return_code=0,
            alloc="0"
        )
        # Slowdown = (10.0 + 5.0) / 5.0 = 3.0
        calc.update(event)
        
        reward = calc.calculate(11.0)
        self.assertEqual(reward, -3.0)
        
        # After calculate, it should clear for the next step
        reward_next = calc.calculate(12.0)
        self.assertEqual(reward_next, 0.0)

    def test_utilization_reward(self):
        calc = UtilizationRewardCalculator(max_resources=10)
        calc.notify_job_started()
        calc.notify_job_started()
        
        reward = calc.calculate(10.0)
        self.assertEqual(reward, 0.2)
        
        event = JobCompletedEvent(
            timestamp=10.0,
            type=EventType.JOB_COMPLETED,
            data={},
            job_id="job_1",
            job_state="COMPLETED",
            return_code=0,
            alloc="0"
        )
        calc.update(event)
        
        reward2 = calc.calculate(11.0)
        self.assertEqual(reward2, 0.1)

    def test_multi_objective(self):
        calc1 = UtilizationRewardCalculator(max_resources=10)
        calc2 = SlowdownRewardCalculator()
        
        multi = MultiObjectiveRewardCalculator([(calc1, 0.5), (calc2, 0.5)])
        
        calc1.notify_job_started()
        calc1.notify_job_started()
        
        event = JobCompletedEvent(
            timestamp=10.0,
            type=EventType.JOB_COMPLETED,
            data={"waiting_time": 10.0, "execution_time": 5.0},
            job_id="job_1",
            job_state="COMPLETED",
            return_code=0,
            alloc="0"
        )
        multi.update(event)
        
        # calc1 = 0.1, calc2 = -3.0
        # total = 0.5 * 0.1 + 0.5 * -3.0 = 0.05 - 1.5 = -1.45
        
        reward = multi.calculate(11.0)
        self.assertAlmostEqual(reward, -1.45)

if __name__ == "__main__":
    unittest.main()
