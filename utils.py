import os, json, uuid
from datetime import datetime
DATA_DIR = "data"
IMAGES_DIR = os.path.join(DATA_DIR, "character_images")
CHATS_DIR = os.path.join(DATA_DIR, "saved_chats")
CHAR_DIR = os.path.join(DATA_DIR, "characters")
def ensure_dirs():
    for d in (DATA_DIR, IMAGES_DIR, CHATS_DIR, CHAR_DIR):
        if not os.path.exists(d):
            os.makedirs(d)
def save_character_json(character_instance, messages):
    ensure_dirs()
    uid = getattr(character_instance, "unique_id", None) or str(uuid.uuid4())
    filename = f"{character_instance.name}_{uid}.json"
    payload = {
        "name": character_instance.name,
        "personality": character_instance.personality,
        "greeting": character_instance.greeting,
        "profile_image_path": character_instance.profile_image_path,
        "model_name": character_instance.model_name,
        "unique_id": uid,
        "messages": messages
    }
    path = os.path.join(CHAR_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path
def save_chat(uid, payload):
    ensure_dirs()
    filename = f"{uid}.json"
    path = os.path.join(CHATS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path
def list_saved_chats():
    ensure_dirs()
    import glob
    return sorted(glob.glob(os.path.join(CHATS_DIR, "*.json")))