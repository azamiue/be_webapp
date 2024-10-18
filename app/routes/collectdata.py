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
    
    if not os.path.exists("embedded_data"):
        os.makedirs("embedded_data")
    
    file_location = f"files/{file.filename}"
    
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    zip_filename_without_extension = os.path.splitext(file.filename)[0]

    extracted_subfolder = os.path.join("extracted", zip_filename_without_extension)
    if not os.path.exists(extracted_subfolder):
        os.makedirs(extracted_subfolder)
    
    embedded_data_subfolder = os.path.join("embedded_data", zip_filename_without_extension)
    if not os.path.exists(embedded_data_subfolder):
        os.makedirs(embedded_data_subfolder)

    try:
        extract_zip(file_location, extracted_subfolder)
    except zipfile.BadZipFile:
        return {"error": "File is not a valid zip file."}

    embeddings,files = embed_images(extracted_subfolder)

    for embedding, file in zip(embeddings, files):
        output_json_path = os.path.join(embedded_data_subfolder, f"{file}.json")
        with open(output_json_path, "w") as json_file:
            json.dump(embedding, json_file) 

    return {
        "info": f"File '{file.filename}' saved and extracted to '{extracted_subfolder}'",
        "embeddings_saved": "embedded_data"
    }
