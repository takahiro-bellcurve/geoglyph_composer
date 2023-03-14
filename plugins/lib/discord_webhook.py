import os, sys
from dotenv import load_dotenv
import requests, json

sys.path.append(os.getenv("BASE_DIR"))
load_dotenv(f"{os.getenv('BASE_DIR')}/.env")


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
    
    def error_notification(self, title, error_message):
        embeds = [
            {
                "title": title,
                "description": f"""
                エラー内容: {error_message}
                """,
                "color": 16711680,
            }
        ]
        self.send(embeds=embeds)

    def scrapy_notification(self, title, spider_name=None, start_time=None, end_time=None, items_scraped=None, error_count=None, error_values=None):
        if error_count == 0:
            embeds = [
                {
                    "title": title,
                    "description": f"""
                    spider名: {spider_name}

                    開始時刻: {start_time}

                    終了時刻: {end_time}

                    Itemを{items_scraped}件取得しました
                    """,
                    "color": 15258703,
                }
            ]
        else:
            embeds = [
                {
                    "title": title,
                    "description": f"""
                    spider名: {spider_name}

                    開始時刻: {start_time}

                    終了時刻: {end_time}

                    Itemを{items_scraped}件取得しました

                    エラー件数: {error_count}

                    エラー内容: {error_values[0:2]}
                    """,
                    "color": 16711680,
                }
            ]
        self.send(embeds=embeds)