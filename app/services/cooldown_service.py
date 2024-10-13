from datetime import datetime, timedelta
from typing import Dict


class CooldownService:
    def __init__(self, cooldown_seconds: int):
        self.cooldown_seconds: int = cooldown_seconds
        self.last_executed: Dict[str, datetime] = {}

    def can_execute(self, action):
        now = datetime.now()
        if action in self.last_executed and (now - self.last_executed[action]) < timedelta(
                seconds=self.cooldown_seconds):
            return False
        self.last_executed[action] = now
        return True

