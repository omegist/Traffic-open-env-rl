#!/usr/bin/env python3
"""
OpenM client for Smart Traffic Intersection.
"""
import os
import requests

ENV_URL = os.getenv("ENV_URL", "http://localhost:8000")


class TrafficClient:
    def __init__(self, base_url: str = ENV_URL):
        self.base_url = base_url.rstrip("/")

    def health(self):
        return requests.get(f"{self.base_url}/health", timeout=10).json()

    def reset(self, difficulty: str = "easy"):
        return requests.post(f"{self.base_url}/reset", params={"difficulty": difficulty}, timeout=10).json()

    def step(self, action_type: str):
        return requests.post(f"{self.base_url}/step", json={"action_type": action_type}, timeout=10).json()

    def grade(self, task: str):
        return requests.post(f"{self.base_url}/grade", params={"task": task}, timeout=30).json()

    def observation_space(self):
        return requests.get(f"{self.base_url}/observation_space", timeout=10).json()

    def action_space(self):
        return requests.get(f"{self.base_url}/action_space", timeout=10).json()


client = TrafficClient()
