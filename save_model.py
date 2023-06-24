from transformers import pipeline

model_checkpoint = "seninoseno/rubert-tiny-vacancy-information-extractor-augumented"
model = pipeline(model=model_checkpoint)
model.save_pretrained("extractor_model")
