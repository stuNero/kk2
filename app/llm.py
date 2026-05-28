from fastapi import FastAPI
from transformers import pipeline

class SmolLM:
    def __init__(self, role, model_name="HuggingFaceTB/SmolLM-135M-Instruct"):
        print(f"Loading {model_name} into memory...")
        try:
            self.pipe = pipeline("text-generation", model_name)
        except:
            raise RuntimeError("Failed to load pipeline")
        print(f"{model_name} successfully loaded!")
    def invoke():
        pass