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
    
    if not os.path.exists("extracted"):
        os.makedirs("extracted")
    
    file_location = f"files/{file.filename}"
    
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    zip_filename_without_extension = os.path.splitext(file.filename)[0]

    extracted_subfolder = os.path.join("extracted", zip_filename_without_extension)
    if not os.path.exists(extracted_subfolder):
        os.makedirs(extracted_subfolder)

    try:
        extract_zip(file_location, extracted_subfolder)
    except zipfile.BadZipFile:
        return {"error": "File is not a valid zip file."}

    embeddings = embed_images(extracted_subfolder)

    output_json_path = os.path.join(extracted_subfolder, f"{zip_filename_without_extension}_embeddings.json")
    with open(output_json_path, "w") as json_file:
        json.dump(embeddings, json_file)

    return {
        "info": f"File '{file.filename}' saved and extracted to '{extracted_subfolder}'",
        "embeddings_saved": output_json_path
    }
