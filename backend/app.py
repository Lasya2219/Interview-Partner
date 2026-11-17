from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.resume_parser import extract_text_from_pdf
import os
from routes.interview import router

app = FastAPI()

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
if not origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/test")
def test():
    return {"message": "Connection Successful"}

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):
    try:
        if not file.filename.endswith(".pdf"):
            return {
                "error": "Only PDF files are allowed."
            }

        file_bytes = await file.read()
        resume_text = extract_text_from_pdf(file_bytes)

        if not resume_text.strip():
            return {
                "error": "No text could be extracted from the uploaded resume."
            }

        return {
            "message": "Resume uploaded successfully",
            "filename": file.filename,
            "text": resume_text
        }

    except Exception as e:
        print(f"Resume Upload Error: {e}")

        return {
            "error": "Failed to process the resume. Please upload a valid PDF."
        }

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)