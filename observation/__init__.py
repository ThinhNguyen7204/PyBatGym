"""
Observation Layer for PyBatGym

1. Design Review:
Maintains state asynchronously via the `ObservationBuilder` interface. 
It extracts and normalizes the state from `BatSimEvent`s passed from the environment, producing `gym.Space` compatible array observations.

2. Code:
Implemented in:
- `base.py`: The `ObservationBuilder` ABC.
- `simple.py`: A `SimpleObservationBuilder` for basic state representations.

3. Usage Example:
```python
from pybatgym.observation.simple import SimpleObservationBuilder

observer = SimpleObservationBuilder(max_jobs=100)
# attach to env config
```
"""

from .base import ObservationBuilder
from .simple import SimpleObservationBuilder

__all__ = ["ObservationBuilder", "SimpleObservationBuilder"]
