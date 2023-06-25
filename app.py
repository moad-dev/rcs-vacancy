from spliting import split
from fastapi import FastAPI
from model import model
from spliting import split
from merge import segmentize_and_merge

app = FastAPI(
    title="Модуль разбиения текстов вакансий",
    description=(
        "Решение представляет собой модуль для разбиения вакансий на должностные обязанности, "
        "требования к соискателю, условия труда и примечания. Модуль может с легкостью встраиваться "
        "в информационные системы агрегации с целью повышения качества оформления предлагаемых объявлений."
    )
)


@app.get(
    "/",
    description="Принимает на вход текст вакансии, возвращает сгруппированные должностные обязанности, "
                "требования к соискателю, условия труда и примечания."
)
async def index(text: str, merged: bool = False) -> dict[str, str]:
    result = {"responsibilities": "",
              "requirements": "",
              "terms": "",
              "notes": ""}

    text = text.replace("\n", " ").replace("\t", " ").replace("\r", "")

    if merged:
        segments = segmentize_and_merge(text)
    else:
        sentences = split(text)
        predicts = [predict["label"] for predict in model.predict(sentences)]
        segments = zip(sentences, predicts)

    for sentence, label in segments:
        result[label.lower()] += sentence + " "
    for key in result.keys():
        result[key] = result[key].strip().replace("  ", " ")

    return result
