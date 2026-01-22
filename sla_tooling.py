import time
import requests

# L'URL de ton application (en local pour l'instant)
URL = "http://localhost:5000" 
SLA_THRESHOLD_MS = 3.0  # La limite de 3ms mentionnée dans ton PDF

def check_sla():
    print(f"--- Vérification de la SLA pour {URL} ---")
    try:
        # Mesurer le temps de réponse
        start_time = time.time()
        response = requests.get(URL)
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        print(f"Temps de réponse: {response_time_ms:.2f} ms")
        
        if response_time_ms <= SLA_THRESHOLD_MS:
            print("Résultat: SLA OK ✅")
        else:
            print(f"Résultat: SLA NOT OK ❌ (Trop lent, limite: {SLA_THRESHOLD_MS}ms)")
            
    except Exception as e:
        print(f"Erreur: Impossible de contacter le serveur. {e}")

if __name__ == "__main__":
    check_sla()