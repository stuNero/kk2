# Package imports
from fastapi    import FastAPI, Body, File, HTTPException, UploadFile
from pydantic   import BaseModel
from io         import StringIO
import pandas   as pd
# Project File imports
from .schema    import UploadResponse, StatsResponse, AskRequest, AskResponse
from .llm.chain import build_chain, PromptBuilderInput

app = FastAPI()
uploaded_dataset: pd.DataFrame = None
# initialise here so patching covers the model in testing
chain = build_chain()


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
    try:
        uploaded_dataset = pd.DataFrame(pd.read_csv(StringIO(contents.decode("utf-8"))))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"invalid CSV format: {str(e)}")
    if len(uploaded_dataset) == 0:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    if len(uploaded_dataset.columns) == 0:
        raise HTTPException(status_code=400, detail="CSV has no columns")

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
    if uploaded_dataset is None:
        raise HTTPException(
            status_code=400,
            detail="Upload a dataset before asking questions"
        )

    try:
        chain_input = PromptBuilderInput(
            question=request.question,
            dataset_stats=uploaded_dataset.describe().to_dict()
        )
        return chain.invoke(chain_input)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: [{str(e)}]")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Model error: [{str(e)}]")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred while processing your question: [{str(e)}]")
