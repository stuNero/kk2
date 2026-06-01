from fastapi import FastAPI, Body, File, HTTPException, UploadFile
from io import StringIO
import pandas as pd
from pydantic import BaseModel

from .llm import SmolLM

app = FastAPI()
llm = SmolLM()

uploaded_dataset: pd.DataFrame = None

@app.get("/health")
def health():
    return {"status":"ok"}

class UploadResponse(BaseModel):
    rows: int
    cols: list[str]
    dtypes: dict[str, str]
    
@app.post("/data/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    global uploaded_dataset
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )
    contents = await file.read()
    uploaded_dataset = pd.DataFrame(pd.read_csv(StringIO(contents.decode("utf-8"))))
    return {
        "rows": len(uploaded_dataset),
        "cols": list(uploaded_dataset.columns),
        "dtypes": uploaded_dataset.dtypes.astype(str).to_dict()
    }

@app.get("/data/stats")
def statistics():
    if uploaded_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return uploaded_dataset.describe().to_dict()

class AskRequest(BaseModel):
    prompt: str
class AskResponse(BaseModel):
    prompt: str
    answer: str
    model: str
    
@app.post("/ai/ask", response_model=AskResponse)
def ask(request: AskRequest):
    return llm.invoke(prompt=request.prompt)