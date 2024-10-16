from fastapi import APIRouter, File, UploadFile
import os, zipfile, json

from services.extract_embedding import extract_zip, embed_images

router = APIRouter()

@router.post("/send-zip")
def receive_zip(file: UploadFile = File(...)):
    if not file.filename.endswith('.zip'):
        return {"error": "File must be a zip file."}

    if not os.path.exists("files"):
        os.makedirs("files")
    
    file_location = f"files/{file.filename}"
    
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # Khởi tạo 1 thư mục chứa file giải nén
    extracted_dir = "extracted"
    try:
        extract_zip(file_location, extracted_dir)  
    except zipfile.BadZipFile:
        return {"error": "File is not a valid zip file."}

    # Embedding các ảnh
    embeddings = embed_images(extracted_dir)

    # Ghi các embedding vào file json
    output_json_path = os.path.join(extracted_dir, "embeddings.json")
    with open(output_json_path, "w") as json_file:
        json.dump(embeddings, json_file)

    return {
        "info": f"File '{file.filename}' saved and extracted to '{extracted_dir}'",
        "embeddings_saved": output_json_path
    }
