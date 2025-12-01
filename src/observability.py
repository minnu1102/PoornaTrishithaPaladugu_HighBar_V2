import os
import json
import logging
import uuid
from datetime import datetime

class RunLogger:
    def __init__(self, run_id=None):
        # Generate a short unique ID for this execution
        self.run_id = run_id or str(uuid.uuid4())[:8]
        
        # Create a dedicated folder for this run
        self.log_dir = f"logs/run_{self.run_id}"
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Configure Internal Logger
        self.logger = logging.getLogger(f"Run_{self.run_id}")
        self.logger.setLevel(logging.INFO)
        
        # File Handler: Saves a timeline of events to execution.jsonl
        fh = logging.FileHandler(f"{self.log_dir}/execution.jsonl")
        formatter = logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        
        print(f" Observability: Logs initialized at {self.log_dir}")

    def log_step(self, agent_name: str, input_data: dict, output_data: dict):
        """
        Saves a detailed trace of a specific agent's action.
        """
        entry = {
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "input_summary": str(input_data)[:500], # Truncate large inputs
            "output": output_data
        }
        
        # Save detailed step log to a specific file (e.g., InsightAgent.json)
        # We append a timestamp to the filename to allow multiple calls to same agent
        step_filename = f"{agent_name}_{datetime.now().strftime('%H%M%S')}.json"
        
        with open(f"{self.log_dir}/{step_filename}", "w") as f:
            json.dump(entry, f, indent=2, default=str)
            
        self.logger.info(f"Executed {agent_name} - Saved trace to {step_filename}")

    def log_error(self, error_msg: str):
        self.logger.error(error_msg)