from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from chains import error_to_caption_chain, select_template, load_faiss_resources
from meme_generator import create_meme
import os
import uuid

app = FastAPI()
# uvicorn main:app --reload

# Load FAISS and embedder once at startup
embedder, index, filenames = load_faiss_resources()

# Define request body model
class ErrorLogRequest(BaseModel):
    error_log: str

@app.post("/generate-meme")
async def generate_meme(request: ErrorLogRequest):
    try:
        error_log = request.error_log.strip()

        # Generate witty caption for the error log
        caption = error_to_caption_chain.run(error_log=error_log).strip()
        print(f"Generated caption: {caption}")

        # Split caption into top and bottom texts (2 lines expected)
        lines = caption.split('\n')
        top_text = lines[0] if len(lines) > 0 else ""
        bottom_text = lines[1] if len(lines) > 1 else ""

        # Select meme template using FAISS-based similarity
        template_filename = select_template(error_log, embedder, index, filenames)

        # Prepare output directory and path
        output_dir = "output_memes"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{uuid.uuid4().hex}.jpg")

        # Generate the meme image with captions
        create_meme(template_filename, top_text, bottom_text, output_path=output_path)

        # Return the generated meme image file
        return FileResponse(output_path, media_type="image/jpeg", filename="generated_meme.jpg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
