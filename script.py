import requests
from bs4 import BeautifulSoup
import os

# 🔹 BYTT UT DISCORD_WEBHOOK_URL med din egen Discord webhook
DISCORD_WEBHOOK_URL = os.getenv(https://discord.com/api/webhooks/1417105343887966218/2SVF8P4BNOiuMZaECRULWkVSA1glkcCPe6SH-v7OoKK_Xq0MKvmIKq29tXe8qXdb6M5m)

# 🔹 BYTT UT LINKEN HER til den brukeren du vil følge
URL = "https://www.nordnet.no/aksjeforum/medlemmer/bagnis"

def fetch_latest_post():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Prøv å finne innleggene (kan måtte tilpasses!)
    posts = soup.find_all("div", class_="message-body")
    if not posts:
        return "Ingen innlegg funnet 🤔"

    latest_post = posts[0].get_text(strip=True)
    return latest_post

def send_discord_message(content):
    data = {"content": content}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Melding sendt til Discord ✅")
    else:
        print("Feil ved sending:", response.text)

if __name__ == "__main__":
    latest = fetch_latest_post()
    send_discord_message(f"Ny melding fra bagnis:\n{latest}")
