import requests
from bs4 import BeautifulSoup
import os

# 🔹 Henter Discord webhook fra GitHub Secrets
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # ikke lim inn selve URLen

# 🔹 BYTT UT LINKEN HER til den brukeren du vil følge
URL = "https://www.nordnet.no/aksjeforum/medlemmer/bagnis"

def fetch_latest_post():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Finn innleggene (må tilpasses hvis Shareville/Nordnet endrer design)
    posts = soup.find_all("div", class_="message-body")  # <- sjekk CSS-klasse!
    if not posts:
        return "Ingen innlegg funnet 🤔"

    latest_post = posts[0].get_text(strip=True)
    return latest_post

def send_discord_message(content):
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook ikke satt opp! ⚠️")
        return

    data = {"content": content}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Melding sendt til Discord ✅")
    else:
        print("Feil ved sending:", response.text)

if __name__ == "__main__":
    latest = fetch_latest_post()
    send_discord_message(f"Ny melding fra bagnis:\n{latest}")
