from fastapi import FastAPI, Body
from llm import SmolLM

app = FastAPI()
llm = SmolLM()

# @app.get("/health")
# def health():
#     return {"status":"ok"}

# @app.post("/data/upload")
# def UploadFile():
#     pass

# @app.get("/data/stats")
# def statistics():
#     pass

@app.post("/ai/ask")
def ask(prompt: str = Body(...)):
    response = llm.invoke(prompt=prompt)
    return response