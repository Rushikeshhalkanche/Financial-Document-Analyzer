from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst, risk_assessor, verifier
from task import analyze_financial_document, verification_task, risk_assessment_task

app = FastAPI(title="Financial Document Analyzer")


def run_crew(query: str, file_path: str):
    financial_crew = Crew(
        agents=[verifier, financial_analyst, risk_assessor],
        tasks=[verification_task, analyze_financial_document, risk_assessment_task],
        process=Process.sequential,
    )

    result = financial_crew.kickoff({
        "query": query,
        "file_path": file_path
    })

    return result


@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Provide investment insights based on this financial document")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        response = run_crew(query=query.strip(), file_path=file_path)

        return {
            "status": "success",
            "analysis": str(response)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)