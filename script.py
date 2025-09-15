import requests
from bs4 import BeautifulSoup
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # hent fra GitHub Secrets
URL = "https://www.nordnet.no/aksjeforum/medlemmer/bagnis"
LAST_POST_FILE = "last_post.txt"  # lagres i repoet midlertidig i Actions

def fetch_latest_post():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    posts = soup.find_all("div", class_="message-body")  # sjekk CSS-klasse
    if not posts:
        return None

    latest_post = posts[0].get_text(strip=True)
    return latest_post

def get_last_sent_post():
    try:
        with open(LAST_POST_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_post(post):
    with open(LAST_POST_FILE, "w", encoding="utf-8") as f:
        f.write(post)

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
    if not latest:
        print("Ingen innlegg funnet 🤔")
        exit()

    last_sent = get_last_sent_post()
    if latest != last_sent:
        send_discord_message(f"Ny melding fra bagnis:\n{latest}")
        save_last_post(latest)
    else:
        print("Ingen nye innlegg, ingen melding sendt.")
