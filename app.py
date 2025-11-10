from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS
from character_base import CharacterAI
import utils, os, json
utils.ensure_dirs()
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
# In-memory registry simple (puede persistir en disk)
INSTANCES = {}
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api/create_character', methods=['POST'])
def create_character():
    body = request.json
    name = body.get('name')
    personality = body.get('personality', '')
    greeting = body.get('greeting', '')
    profile_image = body.get('profile_image_path')  # ruta relativa en data/character_images
    model_name = body.get('model_name', 'gemini-2.0-flash')
    char = CharacterAI(name=name, personality=personality, greeting=greeting,
                       profile_image_path=profile_image, model_name=model_name)
    uid = getattr(char, "unique_id", None) or str(__import__('uuid').uuid4())
    char.unique_id = uid
    INSTANCES[uid] = char
    # primer message
    messages = [{"role": "assistant", "content": greeting, "character": name, "avatar_path": profile_image}]
    return jsonify({"status":"ok","unique_id":uid,"messages":messages})
@app.route('/api/send_message', methods=['POST'])
def send_message():
    body = request.json
    uid = body.get('unique_id')
    text = body.get('text', '')
    if uid not in INSTANCES:
        return jsonify({"status":"error","error":"character not found"}), 404
    char = INSTANCES[uid]
    # opcional: guardar contexto
    char.history.append({"role":"user","content":text})
    resp = char.generate_response(text)
    # append assistant message
    char.history.append({"role":"assistant","content":resp})
    return jsonify({"status":"ok","response":resp, "history": char.history})
@app.route('/api/save_chat', methods=['POST'])
def api_save_chat():
    body = request.json
    uid = body.get('unique_id')
    char = INSTANCES.get(uid)
    if not char:
        return jsonify({"status":"error","error":"character not found"}), 404
    payload = {
        "name": char.name,
        "personality": char.personality,
        "greeting": char.greeting,
        "profile_image_path": char.profile_image_path,
        "model_name": char.model_name,
        "unique_id": char.unique_id,
        "messages": char.history
    }
    path = utils.save_chat(uid, payload)
    return jsonify({"status":"ok","path":path})
# Servir imagenes desde data/
@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory(utils.IMAGES_DIR, filename)
if __name__ == '__main__':
    # modo dev
    app.run(host='0.0.0.0', port=5000, debug=True)