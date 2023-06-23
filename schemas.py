from pydantic import BaseModel
from typing import Optional


class AnnotatedVacancy(BaseModel):
    responsobilities: Optional[str]
    requirements: Optional[str]
    terms: Optional[str]
    skills: Optional[str]
    notes: Optional[str]
