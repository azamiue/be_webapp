from fastapi import APIRouter, File, UploadFile
import os, json
from services.extract_embedding import embed_images
from datetime import datetime
import pytz

router = APIRouter()

@router.get("/embed")
def embed():

    base_folder = "/home/capybara/data/pics/"
    embed_folder = "/home/capybara/data/embed"

    if not os.path.exists(base_folder):
        return {"error": f"Base folder '{base_folder}' does not exist."}
    
    # Tạo thư mục lưu kết quả nhúng (nếu chưa tồn tại)
    if not os.path.exists(embed_folder):
        os.makedirs(embed_folder)

    processed_folders = []
    skipped_folders = []
    errors = []

    # Lấy danh sách thư mục đã tồn tại trong embed
    existing_embeds = set(os.listdir(embed_folder))

    for subfolder in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder)

        if os.path.isdir(subfolder_path) and subfolder not in existing_embeds:
            try:
                # Bỏ qua nếu không phải thư mục
                if not os.path.isdir(subfolder_path):
                    continue
                    
                # Tạo thư mục con trong "embed" tương ứng
                embedded_data_subfolder = os.path.join(embed_folder, subfolder)
                if not os.path.exists(embedded_data_subfolder):
                    os.makedirs(embedded_data_subfolder)

                # Nhúng ảnh từ thư mục con
                embeddings, files = embed_images(subfolder_path)

                # Lưu kết quả nhúng thành file JSON
                for embedding, file in zip(embeddings, files):
                    output_json_path = os.path.join(embedded_data_subfolder, f"{file}.json")
                    with open(output_json_path, "w") as json_file:
                        json.dump(embedding, json_file)

                processed_folders.append(subfolder)
            except Exception as e:
                errors.append({"folder": subfolder, "error": str(e)})
        else:
            skipped_folders.append(subfolder)


    # if os.path.isdir(subfolder_path):
    #     embedded_data_subfolder = os.path.join(embed_folder, subfolder)
    #     if not os.path.exists(embedded_data_subfolder):
    #         os.makedirs(embedded_data_subfolder)

    #     # embedding
    #     embeddings, files = embed_images(subfolder_path)

    #     # save json
    #     for embedding, file in zip(embeddings, files):
    #         output_json_path = os.path.join(embedded_data_subfolder, f"{file}.json")
    #         with open(output_json_path, "w") as json_file:
    #             json.dump(embedding, json_file)
        
    #     processed_folders.append(subfolder)

    result = {
        "info": f"Processed new subfolders in '{base_folder}'.",
        "processed_folders": processed_folders,
        "skipped_folders": skipped_folders,
        "errors": errors,
        "embeddings_saved_to": embed_folder
    }

    # Get the current time in UTC
    utc_now = datetime.now(pytz.utc)

    # Convert to Vietnam timezone
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = utc_now.astimezone(vietnam_tz)

    print("EMBEDDING IN", vietnam_time.strftime('%Y-%m-%d %H:%M:%S'))
    print(json.dumps(result, indent=5, ensure_ascii=False))

    return result