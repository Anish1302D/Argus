"""
Argus - FastAPI application server.
Provides REST API endpoints and serves the interactive adversarial debate web dashboard.
"""

from pathlib import Path
import shutil
import tempfile
from typing import Any, Dict, Optional
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from api.service import SAMPLE_DOCUMENTS, get_service
from trl_core.trl_definitions import get_all_definitions

app = FastAPI(
    title="Argus API",
    description="Evidence-grounded technology readiness assessment with deterministic adjudication and adversarial review synthesis.",
    version="0.1.0",
)

# Enable CORS for external frontends or integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent / "static"
INDEX_HTML = STATIC_DIR / "index.html"


class TextAssessmentRequest(BaseModel):
    text: str
    title: Optional[str] = "Pasted Technical Document"
    strict_security: bool = False


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the interactive web interface."""
    if not INDEX_HTML.exists():
        raise HTTPException(status_code=404, detail="Dashboard UI index.html not found.")
    return FileResponse(INDEX_HTML, media_type="text/html")


@app.get("/api/health")
async def health_check():
    """System health check and engine capability report."""
    return {
        "status": "HEALTHY",
        "version": "0.1.0",
        "competition": "Techfest 2026-27 | 2nd APCTT Hackathon 2026",
        "engine": "Argus evidence-grounded readiness assessment engine",
        "layers": {
            "layer_1_document_processing": "Active (pypdfium2 / UTF-8)",
            "layer_2_ml_inference": "Active (25-dimensional evidence features + deterministic rule adjudication)",
            "layer_3_agent_orchestration": "Active (deterministic Optimist, Skeptic, and Referee review synthesis; no independent LLM agents)",
            "layer_4_web_interface": "Active (FastAPI + static Argus research interface)",
        }
    }


@app.get("/api/trl-ladder")
async def get_trl_ladder():
    """Retrieve full canonical TRL 1-9 framework definitions and criteria."""
    ladder = get_all_definitions()
    return {
        "count": len(ladder),
        "ladder": [lvl.model_dump() for lvl in ladder]
    }


@app.get("/api/sample-documents")
async def list_sample_documents():
    """List preloaded technical test documents."""
    service = get_service()
    return {"samples": service.get_sample_documents()}


@app.post("/api/sample-assess/{sample_id}")
def assess_sample_document(sample_id: str, strict_security: bool = False):
    """Run full assessment on one of the preloaded sample technical papers."""
    if sample_id not in SAMPLE_DOCUMENTS:
        raise HTTPException(status_code=404, detail=f"Sample document '{sample_id}' not found.")
    
    sample = SAMPLE_DOCUMENTS[sample_id]
    service = get_service()
    result = service.assess_text(
        text=sample["content"],
        document_title=sample["title"],
        strict_security=strict_security
    )
    return result


@app.get("/api/sample-assess/{sample_id}/report", response_class=HTMLResponse)
def get_sample_report_html(sample_id: str):
    """Retrieve full exportable technical assessment report for a sample document (Issue 26)."""
    if sample_id not in SAMPLE_DOCUMENTS:
        raise HTTPException(status_code=404, detail=f"Sample document '{sample_id}' not found.")
    sample = SAMPLE_DOCUMENTS[sample_id]
    service = get_service()
    result = service.assess_text(
        text=sample["content"],
        document_title=sample["title"],
        strict_security=False,
    )
    report_md = service.generate_assessment_report(result)
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Argus Technical Assessment Report — {sample_id}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #16150F; background: #F8F6F0; }}
pre {{ background: #ECE7DA; padding: 20px; border-radius: 4px; overflow-x: auto; font-family: monospace; font-size: 0.9em; white-space: pre-wrap; }}
h1, h2, h3 {{ color: #CF4520; }}
</style>
</head>
<body>
<pre>{report_md}</pre>
</body>
</html>"""
    return HTMLResponse(content=html_content)


@app.post("/api/assess-text")
def assess_text_endpoint(req: TextAssessmentRequest):
    """Assess raw technical text directly."""
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Provided document text is empty.")
    service = get_service()
    result = service.assess_text(
        text=req.text,
        document_title=req.title or "Submitted Technical Document",
        strict_security=req.strict_security
    )
    return result


@app.post("/api/assess")
def assess_file_endpoint(
    file: UploadFile = File(...),
    strict_security: bool = Form(False)
):
    """Assess an uploaded technical document file (PDF, TXT, MD)."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")
    
    suffix = Path(file.filename).suffix.lower()
    if suffix not in [".pdf", ".txt", ".md"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file format '{suffix}'. Please upload .pdf, .txt, or .md")

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        service = get_service()
        result = service.assess_file(
            file_path=tmp_path,
            original_filename=file.filename,
            strict_security=strict_security
        )
        return result
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=False)

