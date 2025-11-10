import os
import google.generativeai as genai
class CharacterAI:
    def __init__(self, name, personality, greeting, profile_image_path=None, model_name="gemini-2.0-flash"):
        self.name = name
        self.personality = personality
        self.greeting = greeting
        self.profile_image_path = profile_image_path
        self.model_name = model_name
        self.history = []
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    def generate_response(self, prompt):
        # Petición simple a Gemini; adaptá el parámetro según necesidad
        user_text = f"{self.personality}\\nUsuario: {prompt}\\n{self.name}:"
        try:
            resp = genai.predict(
                model=self.model_name,
                # Ajustá el input según la versión de la API/SDK que uses
                # Aquí usamos el campo "messages" si la librería lo acepta; si falla, adaptá.
                input=user_text
            )
            # resp puede ser dict/obj. Ajustá extracción según la versión del SDK.
            if isinstance(resp, dict) and "candidates" in resp:
                text = resp["candidates"][0].get("content", "")
            else:
                text = str(resp)
        except Exception as e:
            text = f"[ERROR generando respuesta: {e}]"
        self.history.append({"role":"assistant","content":text})
        return text
    def clear_history(self):
        self.history = []