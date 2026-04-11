
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.traffic_environment import TrafficEnv
from server.models import Action
from graders.grader_emergency_response import grade

def run_emergency_response():
    env = TrafficEnv()
    obs = env.reset("medium")
    false_activations = 0
    emergency_events_seen = 0
    done = False
    while not done:
        if obs["emergency_vehicle_present"]:
            action_type = "activate_emergency_mode"
            emergency_events_seen += 1
        elif sum(obs["queues"].values()) > 8:
            action_type = "change_phase"
        else:
            action_type = "extend_green"
        obs, reward, done, info = env.step(Action(action_type=action_type))
        if action_type == "activate_emergency_mode" and not obs.get("emergency_vehicle_present", False):
            false_activations += 1
    output = {
        "emergencies": env.emergencies_handled,
        "false_activations": false_activations,
        "emergency_events_seen": max(emergency_events_seen, 1),
    }
    return grade(output)

GRADER = grade
TASK_ID = "emergency_response"
