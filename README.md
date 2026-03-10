# PyBatGym Framework

A complete, fully functional reinforcement learning-based job scheduling framework for High-Performance Computing (HPC) systems via BatSim and Gymnasium.

## Architecture Principles

- Loose coupling & Dependency inversion
- Testable independent components
- Standard Gymnasium interface compliance
- Modular Observation, Action, and Reward building blocks
- StableBaselines-3 readiness

## Installation

1. Install PyBatGym:
   ```bash
   cd pybatgym
   pip install -e .[dev,examples]
   ```

2. Make sure you have installed [BatSim](https://batsim.readthedocs.io/en/latest/).

## Project Structure

- `envs/`: `Gymnasium.Env` compliant wrappers to control BatSim simulation lifecycle.
- `batsim/`: ZeroMQ adapter, IPC managers, protocol serialization, and simulation event polling.
- `observation/`: Extract structured numeric state spaces (queue statuses, system stats) mapping to `gym.spaces.Box`.
- `action/`: Map generated actions to scheduler execution commands (`EXECUTE_JOB`, `REJECT_JOB`).
- `reward/`: Slowdown logic, utilization formulas, and multi-objective optimizers.
- `config/`: Dataclass-driven test configurations logic.
- `plugins/`: Hook system allowing for independent event tracking (metric aggregators / rendering hooks).
- `wrappers/`: Built-in wrappers to ensure finite time constraints inside BatSim's asynchronous model mapping.

## Examples

Run the example algorithms:

```bash
python examples/train_ppo.py
python examples/train_dqn.py
python examples/evaluate_policy.py
```
