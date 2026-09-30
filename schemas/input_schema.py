from pydantic import BaseModel

class StudentData(BaseModel):
    school: str
    sex: str
    age: int
    studytime: int
    failures: int
    absences: int
    goout: int
    health: int
    # --- ADD THESE MISSING FIELDS ---
    G1: int
    G2: int
    Medu: int
    Fedu: int
    higher: str  # This is "yes" or "no" in the CSV