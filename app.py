from fastapi import FastAPI
from schemas import AnnotatedVacancy

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/annotation", status_code=200)
async def annotation(raw_vacancy: str) -> AnnotatedVacancy:
    return AnnotatedVacancy(
        responsobilities="responsobilities",
        requirements="requirements",
        terms="terms",
        skills="skills",
        notes="notes"
    )
