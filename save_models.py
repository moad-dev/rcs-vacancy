from transformers import pipeline

model_checkpoint = "seninoseno/rubert-base"
model = pipeline(model=model_checkpoint)
model.save_pretrained("model")
