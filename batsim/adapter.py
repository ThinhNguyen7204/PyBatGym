import zmq
import json
import logging
import subprocess
from typing import List, Optional

class BatSimAdapter:
    """Manages BatSim simulation lifespan and bidirectional ZeroMQ communication."""
    
    def __init__(self, endpoint: str = "tcp://*:28000"):
        self.endpoint = endpoint
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.logger = logging.getLogger("BatSimAdapter")
        self._batsim_process: Optional[subprocess.Popen] = None
        self._bound = False

    def start_server(self):
        if not self._bound:
            self.socket.bind(self.endpoint)
            self._bound = True
            self.logger.info(f"Started BatSim ZeroMQ REP server at {self.endpoint}")

    def recv_message(self) -> dict:
        """Receives a REQ message from BatSim and parses it."""
        message = self.socket.recv_string()
        return json.loads(message)

    def send_reply(self, reply: dict):
        """Sends a REP message to BatSim."""
        self.socket.send_string(json.dumps(reply))

    def launch_batsim(self, command: List[str]):
        """Launches BatSim process."""
        self.logger.info(f"Launching BatSim: {' '.join(command)}")
        # Usually command looks like: ['batsim', '-p', 'platform.xml', '-w', 'workload.json', '-e', 'export_dir']
        self._batsim_process = subprocess.Popen(command)

    def is_running(self) -> bool:
        if self._batsim_process is None:
            return False
        return self._batsim_process.poll() is None

    def close(self):
        """Terminates process and closes sockets."""
        if self._batsim_process and self._batsim_process.poll() is None:
            self._batsim_process.terminate()
            self._batsim_process.wait(timeout=5)
        self.socket.close()
        self.context.term()
