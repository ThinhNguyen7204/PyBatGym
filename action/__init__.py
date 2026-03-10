"""
Action Layer for PyBatGym

1. Design Review:
The action layer interfaces between standard `gym.Space` representations and BatSim's protocol payload elements, executing combinations of REJECT, EXECUTE and CALL_ME_LATER actions based on RL outputs. 

2. Code:
Implemented in:
- `base.py`: The abstract `ActionMapper`.
- `discrete.py`: `DiscreteActionMapper` for picking jobs from a queue.

3. Usage Example:
```python
from pybatgym.action.discrete import DiscreteActionMapper

mapper = DiscreteActionMapper(max_queue_size=50)
mapper.update_queue(["job_1", "job_2"])
cmds = mapper.map(0, 10.5) 
# cmds contains [{"type": "EXECUTE_JOB", "data": {"job_id": "job_1", "alloc": "0"}, ...}]
```
"""

from .base import ActionMapper
from .discrete import DiscreteActionMapper

__all__ = ["ActionMapper", "DiscreteActionMapper"]
