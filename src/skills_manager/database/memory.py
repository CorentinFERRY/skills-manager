from typing import List

from skills_manager.models.Learner import Learner
from skills_manager.models.Skill import Skill
from skills_manager.models.Validation import Validation

learners: List[Learner] = []
current_learner_id: int = 1

skills: List[Skill] = []
current_skill_id: int = 1

validations: List[Validation] = []
current_validation_id: int = 1
