from transformers import pipeline

class SmolLM:
    def __init__(self, model_name="HuggingFaceTB/SmolLM-135M-Instruct"):
        print(f"Loading {model_name} into memory...")
        try:
            self.pipe = pipeline("text-generation", model_name)
        except:
            raise RuntimeError("Failed to load pipeline")
        print(f"{model_name} successfully loaded!")
    def invoke(self, prompt:str):
        messages = [
            {"role":"system", "content":"You're a socratic AI tutor"},
            {"role":"user", "content":prompt}
        ]
        output = self.pipe(messages, max_new_tokens=500)
        return output[0]['generated_text'][-1]['content']

llm = SmolLM()

print(llm.invoke(prompt="explain in 2 sentences: what is a gpt?"))