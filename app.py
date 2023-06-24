from spliting import split
from fastapi import FastAPI
import torch
from transformers import pipeline


app = FastAPI(
    title="Модуль разбиения текстов вакансий",
    description="Решение представляет собой модуль для разбиения вакансий на должностные обязанности, "
                "требования к соискателю, условия труда и примечания. Модуль может с легкостью встраиваться "
                "в информационные системы агрегации с целью повышения качества оформления предлагаемых объявлений."
)

device = torch.cuda.current_device() if torch.cuda.is_available() and torch.cuda.mem_get_info()[0] >= 2*1024**3 else -1
model = pipeline("text-classification", "extractor_model", device=device)


@app.get("/", description="Принимает на вход текст вакансии, возвращает сгруппированные должностные обязанности, "
                        "требования к соискателю, условия труда и примечания.")
async def index(text: str) -> dict[str, str]:
    result = {"responsibilities": "",
              "requirements": "",
              "terms": "",
              "notes": ""}
    text = text.replace("\n", " ").replace("\t", " ").replace("\r", "")
    sentences = split(text)
    predicts = [predict["label"] for predict in model.predict(sentences)]
    for sentence, label in zip(sentences, predicts):
        result[label.lower()] += sentence + " "
    for key in result.keys():
        result[key] = result[key].strip().replace("  ", " ")
    return result
