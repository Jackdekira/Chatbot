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
        try:
            model = genai.GenerativeModel(self.model_name)

            # Construcción del mensaje final para el modelo
            user_text = (
                f"Contexto del personaje:\n{self.personality}\n\n"
                f"Historial reciente:\n{self.history}\n\n"
                f"Usuario: {prompt}\n"
                f"{self.name}:"
            )

            response = model.generate_content([user_text])

            # El SDK expone el texto siempre como response.text
            text = response.text if hasattr(response, "text") else str(response)

        except Exception as e:
            text = f"[ERROR generando respuesta: {e}]"

        self.history.append({"role": "assistant", "content": text})
        return text
    def clear_history(self):
        self.history = []