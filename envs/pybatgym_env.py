import gymnasium as gym
from gymnasium import spaces
import numpy as np
import logging
from typing import Optional, Tuple, Dict, Any

from pybatgym.batsim.adapter import BatSimAdapter
from pybatgym.batsim.protocol import BatSimProtocol
from pybatgym.batsim.events import parse_event, EventType

class PyBatGymEnv(gym.Env):
    """
    Main Gymnasium environment for PyBatGym.
    
    This environment acts as the RL interface to the BatSim scheduler.
    It expects modular implementations for observation, action, and reward.
    """
    
    metadata = {"render_modes": ["ansi"]}
    
    def __init__(self, 
                 batsim_command: list[str],
                 batsim_endpoint: str = "tcp://*:28000",
                 observation_builder=None,
                 action_mapper=None,
                 reward_calculator=None,
                 render_mode: Optional[str] = None):
        super().__init__()
        
        self.logger = logging.getLogger("PyBatGymEnv")
        
        # Core components
        self.batsim_command = batsim_command
        self.adapter = BatSimAdapter(endpoint=batsim_endpoint)
        
        # These will be implemented in subsequent modules
        self.observation_builder = observation_builder
        self.action_mapper = action_mapper
        self.reward_calculator = reward_calculator
        
        self.render_mode = render_mode
        self.current_time = 0.0
        self.simulation_ended = False
        
        # Will be initialized based on builder/mapper components
        # Currently placeholders
        self.action_space = spaces.Discrete(1) if not action_mapper else action_mapper.get_space()
        self.observation_space = spaces.Box(low=0, high=1, shape=(1,)) if not observation_builder else observation_builder.get_space()

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> Tuple[Any, dict]:
        """Resets the environment for a new episode."""
        super().reset(seed=seed)
        
        if self.adapter.is_running():
            self.adapter.close()
            
        self.adapter.start_server()
        self.adapter.launch_batsim(self.batsim_command)
        
        self.current_time = 0.0
        self.simulation_ended = False
        
        if self.observation_builder:
            self.observation_builder.reset()
        if self.action_mapper:
            self.action_mapper.reset()
        if self.reward_calculator:
            self.reward_calculator.reset()
            
        # Initial step to wait for SIMULATION_BEGIN
        self._step_simulation([])
            
        info = {"current_time": self.current_time}
        observation = self._get_observation()
        
        return observation, info

    def step(self, action: Any) -> Tuple[Any, float, bool, bool, dict]:
        """Steps the environment by applying an action."""
        if self.simulation_ended:
            return self._get_observation(), 0.0, True, False, {"error": "Simulation already ended"}
            
        # 1. Map action to BatSim commands (events to send back)
        batsim_cmds = []
        if self.action_mapper:
            batsim_cmds = self.action_mapper.map(action, self.current_time)
            
        # 2. Advance simulation (send commands, receive new state)
        self._step_simulation(batsim_cmds)
        
        # 3. Calculate metrics
        observation = self._get_observation()
        reward = 0.0
        if self.reward_calculator:
            reward = self.reward_calculator.calculate(self.current_time)
            
        terminated = self.simulation_ended
        truncated = False # Can be managed by TimeLimit wrappers
        info = {"current_time": self.current_time}
        
        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "ansi":
            print(f"Time: {self.current_time}, Simulation Ended: {self.simulation_ended}")

    def close(self):
        self.adapter.close()
        
    def _step_simulation(self, reply_events: list[dict]):
        """Communicates with BatSim to advance time and receive events."""
        reply = BatSimProtocol.build_reply(self.current_time, reply_events)
        self.adapter.send_reply(reply)
        
        msg = self.adapter.recv_message()
        now, events_raw = BatSimProtocol.parse_message(msg)
        self.current_time = now
        
        for raw_event in events_raw:
            event = parse_event(raw_event)
            if event.type == EventType.SIMULATION_ENDS:
                self.simulation_ended = True
            
            # Pass events to builders to update their states
            if self.observation_builder:
                self.observation_builder.update(event)
            if self.reward_calculator:
                self.reward_calculator.update(event)

    def _get_observation(self) -> Any:
        if self.observation_builder:
            return self.observation_builder.get_observation()
        return np.zeros(self.observation_space.shape, dtype=self.observation_space.dtype)
