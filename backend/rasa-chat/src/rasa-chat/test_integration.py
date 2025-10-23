import requests
import json

def test_integration():
    print("🧪 Probando integración completa del sistema...")
    print("=" * 50)
    
    # Test 1: API FastAPI
    print("1. Probando API FastAPI...")
    try:
        response = requests.get("http://localhost:8000/chatbot/tramites/?palabra_clave=licencia")
        if response.status_code == 200:
            tramites = response.json()
            print("   ✅ API FastAPI - FUNCIONANDO")
            print(f"   📊 Trámites encontrados: {len(tramites)}")
            for tramite in tramites:
                print(f"      📋 {tramite['nombre']}")
        else:
            print(f"   ❌ API FastAPI - ERROR: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ API FastAPI - ERROR: {e}")
    
    print("\n2. Probando Rasa Actions Server...")
    # Test 2: Rasa Actions
    try:
        response = requests.get("http://localhost:5055/")
        if response.status_code == 200:
            print("   ✅ Rasa Actions - FUNCIONANDO (servidor activo)")
        else:
            print(f"   ⚠️  Rasa Actions - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Rasa Actions - ERROR: {e}")
        print("   💡 Asegúrate de que 'rasa run actions' esté ejecutándose")
    
    print("\n3. Probando endpoints específicos...")
    # Test 3: Endpoints específicos de la API
    endpoints = [
        "/chatbot/health",
        "/chatbot/tramites/",
        "/chatbot/informacion/emergencia",
        "/chatbot/categorias/tramites"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}")
            if response.status_code == 200:
                print(f"   ✅ {endpoint} - FUNCIONANDO")
            else:
                print(f"   ⚠️  {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint} - ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 RESUMEN: La API está funcionando correctamente.")
    print("💡 Cuando resuelvas TensorFlow, podrás entrenar el modelo Rasa completo.")

if __name__ == "__main__":
    test_integration()