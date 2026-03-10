"""
BatSim Integration Module for PyBatGym

1. Design Review:
This module acts as the lowest-level interface to the external BatSim scheduling simulator. 
It follows a standard Server design using ZeroMQ. BatSim connects to this adapter as a REQ via IPC/TCP.
The simulator sends simulation events (Job Arrival, Job Completion) to the Python process.
The Python side decodes these using `protocol.py` and maps them to standard Dataclasses in `events.py`.
The scheduler logic can then respond using the `adapter.py`'s send mechanism.

2. Code:
Implemented in:
- adapter.py: `BatSimAdapter` to manage ZeroMQ sockets and subprocesses.
- events.py: Event types and parsing layer.
- protocol.py: Builders for JSON commands BatSim expects.

3. Usage Example:
```python
from pybatgym.batsim.adapter import BatSimAdapter
from pybatgym.batsim.protocol import BatSimProtocol

adapter = BatSimAdapter("tcp://*:28000")
adapter.start_server()
adapter.launch_batsim(["batsim", "-p", "platform.xml", "-w", "workload.json"])

while adapter.is_running():
    msg = adapter.recv_message()
    now, events = BatSimProtocol.parse_message(msg)
    
    # Process events and prepare reply
    reply = BatSimProtocol.build_reply(now, [])
    adapter.send_reply(reply)
    
adapter.close()
```

4. Testing Snippet:
See `tests/test_batsim_module.py` for integration testing of the mock BatSim communication. 
"""

from .adapter import BatSimAdapter
from .events import EventType, BatSimEvent, parse_event
from .protocol import BatSimProtocol

__all__ = ["BatSimAdapter", "EventType", "BatSimEvent", "parse_event", "BatSimProtocol"]
