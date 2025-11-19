import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

print(f"API Key encontrada: {api_key[:20]}..." if api_key else "API Key NÃO encontrada!")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Lista os modelos disponíveis
        print("\n📋 Modelos disponíveis:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  ✅ {model.name}")
        
        # Testa com um modelo
        print("\n🧪 Testando geração de conteúdo...")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Diga olá em uma palavra")
        print(f"✅ Resposta: {response.text}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
else:
    print("❌ Configure a API Key no arquivo .env")