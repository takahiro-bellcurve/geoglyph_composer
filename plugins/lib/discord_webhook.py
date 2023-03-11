import os, sys
from dotenv import load_dotenv
import requests, json

load_dotenv(".env")
sys.path.append(os.getenv("BASE_DIR"))


class DiscordWebhook:
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    def send(self, content=None, tts=False, embeds=None):
        payload = {"content": content, "tts": tts, "embeds": embeds}

        headers = {"Content-Type": "application/json"}
        res = requests.post(self.webhook_url, json=payload, headers=headers)
        if res.status_code != 204:
            raise Exception(
                f"Failed to send message to discord webhook. Status code: {res.status_code}"
            )
        return res.status_code
