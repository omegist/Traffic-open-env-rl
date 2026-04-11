
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.traffic_environment import TrafficEnv
from server.models import Action
from graders.grader_phase_management import grade

def run_phase_management():
    env = TrafficEnv()
    obs = env.reset("easy")
    phase_changes = 0
    unnecessary_phase_changes = 0
    done = False
    while not done:
        if sum(obs["queues"].values()) > 8:
            action_type = "change_phase"
        else:
            action_type = "extend_green"
        obs, reward, done, info = env.step(Action(action_type=action_type))
        if action_type == "change_phase":
            phase_changes += 1
            if sum(obs["queues"].values()) < 4:
                unnecessary_phase_changes += 1
    output = {
        "throughput": env.throughput,
        "unnecessary_phase_changes": unnecessary_phase_changes,
        "phase_changes": phase_changes,
    }
    return grade(output)

GRADER = grade
TASK_ID = "phase_management"
