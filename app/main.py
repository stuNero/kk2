# Package imports
from fastapi    import FastAPI, Body, File, HTTPException, UploadFile
from pydantic   import BaseModel
from io         import StringIO
import pandas as pd
# Project File imports
from .llm   import SmolLM
from .schema import UploadResponse, StatsResponse, AskRequest, AskResponse

app = FastAPI()
llm = SmolLM()

uploaded_dataset: pd.DataFrame = None

@app.get("/health")
def health():
    return {"status":"ok"}
    
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

@app.get("/data/stats", response_model=StatsResponse)
def statistics():
    if uploaded_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    return {"stats": uploaded_dataset.describe().to_dict()}

@app.post("/ai/ask", response_model=AskResponse)
def ask(request: AskRequest):
    return llm.invoke(prompt=request.prompt)
