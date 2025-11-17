import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import create_document, get_documents, db
from schemas import Inquiry

app = FastAPI(title="Plumber Site API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Plumber API up"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test")
def test_database():
    response = {
        "backend": "running",
        "database": "disconnected",
        "collections": [],
    }
    try:
        if db is not None:
            response["database"] = "connected"
            try:
                response["collections"] = db.list_collection_names()[:10]
            except Exception as e:
                response["database"] = f"connected_with_error: {str(e)[:80]}"
    except Exception as e:
        response["database"] = f"error: {str(e)[:80]}"
    return response

class InquiryResponse(BaseModel):
    id: str

@app.post("/inquiry", response_model=InquiryResponse)
def create_inquiry(inquiry: Inquiry):
    try:
        inserted_id = create_document("inquiry", inquiry)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/inquiries")
def list_inquiries(limit: Optional[int] = 50):
    try:
        docs = get_documents("inquiry", limit=limit)
        # Convert ObjectId to str if present
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
