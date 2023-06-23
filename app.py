from fastapi import FastAPI
from razdel import sentenize
import torch
from transformers import pipeline

app = FastAPI()

device = torch.cuda.current_device() if torch.cuda.is_available() and torch.cuda.mem_get_info()[0] >= 2*1024**3 else -1
model = pipeline("text-classification", "model", device=device)


@app.get("/")
async def index(text: str):
    result = {"responsibilities": "",
              "requirements": "",
              "terms": "",
              "notes": ""}
    text = text.replace("\n", " ").replace("\t", " ").replace("\r", "")
    sentences = [sentence.text for sentence in sentenize(text)]
    predicts = [predict["label"] for predict in model.predict(sentences)]
    for sentence, label in zip(sentences, predicts):
        result[label.lower()] += sentence + " "
    return result
