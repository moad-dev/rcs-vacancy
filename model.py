import torch
from transformers import pipeline


device = (
    torch.cuda.current_device()
    if torch.cuda.is_available() and torch.cuda.mem_get_info()[0] >= 2*1024**3
    else -1
)

model = pipeline("text-classification", "extractor_model", device=device)
