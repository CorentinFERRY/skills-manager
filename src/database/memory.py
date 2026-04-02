from typing import List

from src.models.Learner import Learner
from src.models.Skill import Skill
from src.models.Validation import Validation

learners: List[Learner] = []
current_learner_id: int = 1

skills: List[Skill] = []
current_skill_id: int = 1

validations: List[Validation] = []
current_validation_id: int = 1
