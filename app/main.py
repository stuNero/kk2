from fastapi import FastAPI, Body, File, HTTPException, UploadFile
from io import StringIO
import pandas as pd

from .llm import SmolLM

app = FastAPI()
llm = SmolLM()

uploaded_dataset: pd.DataFrame = None

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/data/upload")
async def upload_file(file: UploadFile = File(...)):
    global uploaded_dataset

    contents = await file.read()
    uploaded_dataset = pd.read_csv(StringIO(contents.decode("utf-8")))

    return {
        "filename": file.filename,
        "rows": len(uploaded_dataset),
        "columns": list(uploaded_dataset.columns),
    }

@app.get("/data/stats")
def statistics():
    if uploaded_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return uploaded_dataset.describe().to_dict()

@app.post("/ai/ask")
def ask(prompt: str = Body(...)):
    response = llm.invoke(prompt=prompt)
    return response