
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.traffic_environment import TrafficEnv
from server.models import Action
from graders.grader_queue_optimization import grade

def run_queue_optimization():
    env = TrafficEnv()
    obs = env.reset("hard")
    queue_sum = 0
    step_count = 0
    done = False
    while not done:
        if sum(obs["queues"].values()) > 6:
            action_type = "change_phase"
        else:
            action_type = "extend_green"
        obs, reward, done, info = env.step(Action(action_type=action_type))
        queue_sum += sum(obs["queues"].values())
        step_count += 1
    avg_queue = queue_sum / max(step_count, 1)
    final_queue = sum(env.queues.values())
    output = {
        "throughput": env.throughput,
        "avg_queue": avg_queue,
        "final_queue": final_queue,
    }
    return grade(output)

GRADER = grade
TASK_ID = "queue_optimization"
