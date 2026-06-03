# Kunskapskontroll 2 AI-programmering Python Course
This is a graded project for a school course. 

## Description
This is a fastapi backend with an AI chatbot ➡️`SmolLM2-360M-Instruct`. 
You are able to upload a CSV dataset of your choice and ask the bot questions about it.
You are also able to manually check the stats of your dataset. 

## Prerequisites
- `Git Bash`, `powershell` or any other shell
- `uv` from astral -> https://docs.astral.sh/uv/
- `Python 3.14`+

## How to run:
1. Clone repository ➡️`git clone git@github.com:stuNero/kk2.git` and navigate to repo root 
2. In terminal, run:
```shell
uv sync
fastapi dev
```
3. Verify server running by visiting `http://localhost:8000/health`

### Swagger
`http://localhost:8000/docs` to test following endpoints interactively

### Endpoints
- ``/health``
    - Checks if server is running and communicating
- `/data/upload`
    - Uploads a .csv dataset of your choice
    - Does not accept any other file format
- `/data/stats`
    - Gives you a breakdown of the statistics of the dataset
- `/ai/ask`
    - You can ask questions about your uploaded dataset