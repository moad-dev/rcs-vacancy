from transformers import pipeline

model_checkpoint = "seninoseno/rubert-tiny-vacancy-information-extractor"
model = pipeline(model=model_checkpoint)
model.save_pretrained("model")
