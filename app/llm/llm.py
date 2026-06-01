from transformers import pipeline

class SmolLM:
    def __init__(self, model_name="HuggingFaceTB/SmolLM2-360M-Instruct"):
        self.model_name = model_name
        print(f"Loading {model_name} into memory...")
        try:
            self.pipe = pipeline("text-generation", model_name)
        except Exception as exc:
            raise RuntimeError("Failed to load pipeline") from exc
        print(f"{model_name} successfully loaded!")
    def invoke(self, prompt: str) -> str:
        messages = [
            {"role":"system", "content":"You're a socratic AI tutor"},
            {"role":"user", "content":prompt}
        ]
        output = self.pipe(messages, max_new_tokens=500)
        return output[0]["generated_text"][-1]["content"]
