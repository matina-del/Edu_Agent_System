from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class KnowledgePoint:
    id: str
    name: str
    subject: str
    mastery_level: float = 0.0

@dataclass
class UserProfile:
    user_id: str
    name: str
    grade: str
    subjects: List[str]
    knowledge_points: Dict[str, KnowledgePoint] = field(default_factory=dict)
    learning_history: List[dict] = field(default_factory=list)
    weak_points: List[str] = field(default_factory=list)
    strong_points: List[str] = field(default_factory=list)
    
    def update_mastery(self, kp_id: str, delta: float):
        if kp_id in self.knowledge_points:
            current = self.knowledge_points[kp_id].mastery_level
            self.knowledge_points[kp_id].mastery_level = current * 0.7 + delta * 0.3
            if self.knowledge_points[kp_id].mastery_level < 0.4:
                if kp_id not in self.weak_points: self.weak_points.append(kp_id)
            elif self.knowledge_points[kp_id].mastery_level > 0.8:
                if kp_id not in self.strong_points: self.strong_points.append(kp_id)

class UserProfileManager:
    def __init__(self):
        self.profiles: Dict[str, UserProfile] = {}
    
    def get_or_create_profile(self, user_id: str) -> UserProfile:
        if user_id not in self.profiles:
            self.profiles[user_id] = UserProfile(user_id=user_id, name="TestUser", grade="初二", subjects=["数学"])
        return self.profiles[user_id]
        