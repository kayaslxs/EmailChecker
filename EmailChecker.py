import requests
import sys
import os
from pyfiglet import Figlet
from termcolor import colored

# API URL'si
BASE_URL = "https://mailscrap.com/api/verifier-lookup/"

def clear_screen():
    """Terminal ekranını temizler."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """ASCII sanat başlığını ve imzayı gösterir."""
    f = Figlet(font='chunky')  # Kalın font seçeneği
    
    # Başlık
    ascii_art = f.renderText('EMAIL CHECKER')
    print(colored(ascii_art, 'cyan', attrs=['bold']))
    
    # İmza
    print(colored("by KAYA SLXS\n", 'magenta', attrs=['bold']))
    print("-" * 70)

def get_status_text(value):
    """Durum değerine göre renkli metin döndürür."""
    if value is True:
        return colored("✅ Yes", 'green')
    elif value is False:
        return colored("❌ No", 'red')
    else:
        return colored(str(value), 'yellow')

def check_email_cli(email_address: str):
    """Verilen e-posta adresini API ile kontrol eder ve sonucu yazdırır."""
    
    print(colored(f"\n🔎 Checking Address: {email_address}...", 'yellow'))
    
    try:
        # API çağrısı
        url = f"{BASE_URL}{email_address}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        print(colored("\n--- Result Details ---", 'blue', attrs=['bold']))
        
        # Genel Durum
        api_success = get_status_text(data.get("success"))
        deliverable = get_status_text(data.get("deliverable"))
        
        print(f"Success:            {api_success}")
        print(f"Deliverable Status: {deliverable}")
        print(colored("--------------------------", 'blue'))
        
        # Detaylar
        print(f"Valid Format:       {get_status_text(data.get('valid-format'))}")
        print(f"Disposable:         {get_status_text(data.get('disposable'))}")
        print(f"Role-Based:         {get_status_text(data.get('role-base'))}")
        print(f"Free Mail:          {get_status_text(data.get('free-mail'))}")
        print(f"Server Status:      {get_status_text(data.get('server-status'))}")
        print(f"Domain:             {colored(data.get('email-domain', 'N/A'), 'white', attrs=['bold'])}")
        print(f"User:               {colored(data.get('email-user', 'N/A'), 'white', attrs=['bold'])}")
        print(colored("--------------------------\n", 'blue'))

    except requests.exceptions.RequestException as e:
        print(colored(f"\n❌ Bağlantı Hatası: API'ye ulaşılamadı veya zaman aşımı. Detay: {e}", 'red'))
    except Exception as e:
        print(colored(f"\n❌ Beklenmedik Hata: {e}", 'red'))

def main():
    """Ana program akışını yönetir."""
    clear_screen()
    display_header()
    
    while True:
        try:
            # Kullanıcıdan e-posta adresi isteme
            email_to_check = input(colored("Enter Email Address: ", 'green', attrs=['bold'])).strip()
            
            if email_to_check.lower() in ['quit', 'exit', 'q']:
                break
            
            if not email_to_check:
                print(colored("Please enter a valid email address.", 'red'))
                continue
                
            check_email_cli(email_to_check)
            
        except KeyboardInterrupt:
            # Ctrl+C ile çıkış
            break
        except Exception as e:
            print(colored(f"An error occurred during input: {e}", 'red'))
            break

if __name__ == "__main__":
    try:
        main()
    finally:
        print(colored("Application finished. Goodbye!", 'yellow'))