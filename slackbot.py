import asyncio
import logging
import os
from dotenv import find_dotenv, load_dotenv
import requests
from logger import get_logger
logger = get_logger(__name__)
# Load environment variables from the root .env file
root_env_path = find_dotenv()
load_dotenv(root_env_path)

SLACKBOT_WEBHOOK_URL = os.getenv("SLACKBOT_WEBHOOK_URL")

class SlackBot:
    def __init__(self, webhook_url: str) -> None:
        self.webhookURL = webhook_url
        return None

    async def send_message(self, message: str):
        try:
            logging.info("try to sent data to slack")
            payload = {"text": message}
            response = requests.post(self.webhookURL, json=payload)
            if response.status_code == 200:
                logging.info("sucessfully sent data to slack")
            else:
                logging.error(f"Error: Send to slack failed with status code: {response.status_code}")
        except Exception as error:
            logging.info("An error occurred while sending message to slack: ", error)
            return


SHAI_Slack_Bot = SlackBot(SLACKBOT_WEBHOOK_URL)

if __name__ == "__main__":
    asyncio.run(SHAI_Slack_Bot.send_message("sending test message from script"))