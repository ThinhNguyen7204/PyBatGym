import unittest
import os
import json
import tempfile
from pybatgym.config import load_config_from_json, EnvironmentConfig, ClusterConfig, WorkloadConfig

class TestConfigModule(unittest.TestCase):

    def test_load_from_json(self):
        config_data = {
            "batsim_endpoint": "tcp://*:28001",
            "cluster": {
                "platform_file": "plat.xml",
                "num_resources": 4
            },
            "workload": {
                "workload_file": "work.json"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            filepath = f.name
            
        try:
            config = load_config_from_json(filepath)
            self.assertEqual(config.batsim_endpoint, "tcp://*:28001")
            self.assertEqual(config.cluster.num_resources, 4)
            self.assertEqual(config.cluster.platform_file, "plat.xml")
            
            cmd = config.get_batsim_command()
            self.assertIn("-p", cmd)
            self.assertIn("plat.xml", cmd)
            self.assertIn("-s", cmd)
            self.assertIn("tcp://*:28001", cmd)
            
        finally:
            os.remove(filepath)

if __name__ == "__main__":
    unittest.main()
