import os
import openai
import google.generativeai as genai

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

    def get_completion(self, prompt, provider="openai", model="gpt-3.5-turbo", temperature=0.7):
        if provider == "openai":
            if not self.openai_api_key:
                return {"error": "Chave da API OpenAI não configurada"}
            try:
                response = openai.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )
                return {"output": response.choices[0].message.content}
            except Exception as e:
                return {"error": f"Erro na API OpenAI: {str(e)}"}
        elif provider == "gemini":
            if not self.gemini_api_key:
                return {"error": "Chave da API Gemini não configurada"}
            try:
                model_gemini = genai.GenerativeModel(model)
                response = model_gemini.generate_content(prompt)
                return {"output": response.text}
            except Exception as e:
                return {"error": f"Erro na API Gemini: {str(e)}"}
        else:
            return {"error": "Provedor de IA não suportado"}

    def analyze_data(self, data, provider="openai", model="gpt-3.5-turbo", instructions="Analise os dados e forneça insights."):
        prompt = f"{instructions}\nDados: {data}"
        return self.get_completion(prompt, provider, model)

    def generate_content(self, topic, provider="openai", model="gpt-3.5-turbo", instructions="Gere conteúdo sobre o tópico."):
        prompt = f"{instructions}\nTópico: {topic}"
        return self.get_completion(prompt, provider, model)


