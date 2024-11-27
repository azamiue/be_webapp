from fastapi import APIRouter, BackgroundTasks
import os, json
from services.extract_embedding import embed_images
from datetime import datetime
import pytz

router = APIRouter()

def process_embedding(base_folder: str, embed_folder: str):
    if not os.path.exists(base_folder):
        print(f"Base folder '{base_folder}' does not exist.")
        return

    if not os.path.exists(embed_folder):
        os.makedirs(embed_folder)

    processed_folders = []
    skipped_folders = []
    errors = []

    existing_embeds = set(os.listdir(embed_folder))

    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)

        if os.path.isdir(subfolder_path) and subfolder not in existing_embeds:
            try:
                if not os.path.isdir(subfolder_path):
                    continue

                embedded_data_subfolder = os.path.join(embed_folder, subfolder)
                if not os.path.exists(embedded_data_subfolder):
                    os.makedirs(embedded_data_subfolder)

                embeddings, files = embed_images(subfolder_path)

                for embedding, file in zip(embeddings, files):
                    output_json_path = os.path.join(embedded_data_subfolder, f"{file}.json")
                    with open(output_json_path, "w") as json_file:
                        json.dump(embedding, json_file)

                print("embed successfully", subfolder)
                processed_folders.append(subfolder)
            except Exception as e:
                errors.append({"folder": subfolder, "error": str(e)})
        else:
            print("skipped folder", subfolder)
            skipped_folders.append(subfolder)

    utc_now = datetime.now(pytz.utc)
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    vietnam_time = utc_now.astimezone(vietnam_tz)

    result = {
        "info": f"Processed new subfolders in '{base_folder}'.",
        "processed_folders": processed_folders,
        "skipped_folders": skipped_folders,
        "errors": errors,
        "embeddings_saved_to": embed_folder,
        "timestamp": vietnam_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    print(json.dumps(result, indent=5, ensure_ascii=False))

@router.get("/embed")
def embed(background_tasks: BackgroundTasks):
    base_folder = "/home/capybara/data/pics/"
    embed_folder = "/home/capybara/data/embed"

    background_tasks.add_task(process_embedding, base_folder, embed_folder)

    return {"message": "Embedding task started. Check logs or embed folder for updates."}
