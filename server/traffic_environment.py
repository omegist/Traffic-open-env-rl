import random
import uuid

try:
    from openenv.core.env_server import Environment
    HAS_OPENENV = True
except ImportError:
    HAS_OPENENV = False

try:
    from ..models import LightPhase, Action, Observation, State
except ImportError:
    from models import LightPhase, Action, Observation, State


class TrafficEnv:
    def __init__(self):
        self._reset_state()

    def _reset_state(self):
        self.difficulty = "easy"
        self.rate = 0.1
        self.queues = {"North": 0, "South": 0, "East": 0, "West": 0}
        self.phase = LightPhase.NS_GREEN
        self.emergency_present = False
        self.emergency_dir = None
        self.step_count = 0
        self.throughput = 0
        self.emergencies_handled = 0
        self.episode_id = str(uuid.uuid4())

    def reset(self, difficulty: str = "easy") -> dict:
        self._reset_state()
        self.difficulty = difficulty
        self.rate = {"easy": 0.1, "medium": 0.3, "hard": 0.5}.get(difficulty, 0.1)
        return self._obs()

    def _obs(self) -> dict:
        return {
            "queues": dict(self.queues),
            "current_phase": self.phase.value,
            "emergency_vehicle_present": self.emergency_present,
            "emergency_direction": self.emergency_dir,
            "step_count": self.step_count,
        }

    def state(self) -> dict:
        return {
            "queues": dict(self.queues),
            "phase": self.phase.value,
            "emergency_present": self.emergency_present,
            "emergency_dir": self.emergency_dir,
            "step_count": self.step_count,
            "throughput": self.throughput,
            "emergencies_handled": self.emergencies_handled,
            "episode_id": self.episode_id,
        }

    def step(self, action) -> tuple:
        action_type = action.action_type if hasattr(action, "action_type") else action
        self.step_count += 1
        reward = 0.0

        if action_type == "change_phase":
            self.phase = (LightPhase.EW_GREEN
                          if self.phase == LightPhase.NS_GREEN
                          else LightPhase.NS_GREEN)
            reward -= 1.0
        elif action_type == "extend_green":
            dirs = (["North", "South"] if self.phase == LightPhase.NS_GREEN
                    else ["East", "West"])
            for d in dirs:
                cleared = min(self.queues[d], 2)
                self.queues[d] -= cleared
                self.throughput += cleared
            reward += 0.5
        elif action_type == "activate_emergency_mode":
            if self.emergency_present:
                reward += 15.0
                self.emergencies_handled += 1
                self.emergency_present = False
                self.emergency_dir = None
            else:
                reward -= 10.0

        green_dirs = (["North", "South"] if self.phase == LightPhase.NS_GREEN
                      else ["East", "West"])
        for d in green_dirs:
            if self.queues[d] > 0:
                self.queues[d] -= 1
                self.throughput += 1

        for d in self.queues:
            if random.random() < self.rate:
                self.queues[d] += 1

        if not self.emergency_present and random.random() < 0.05:
            self.emergency_present = True
            self.emergency_dir = random.choice(list(self.queues.keys()))

        done = self.step_count >= 100
        info = {"throughput": self.throughput, "emergencies": self.emergencies_handled}
        return self._obs(), reward, done, info
