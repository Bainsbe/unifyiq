from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from api.assistant import skill_q_and_a
from utils.constants import SLACK
from utils.database import unifyiq_config_db
from utils.database.unifyiq_config_db import get_slack_app_token, get_slack_bot_token

source_configs = unifyiq_config_db.get_fetcher_configs()
app = None
for source_config in source_configs:
    if source_config.connector_type == SLACK:
        # Initialize your app with your bot token
        app = App(token=get_slack_bot_token(source_config.config_json))
        break
if not app:
    raise Exception("No slack app found. Cannot start slack bot.")


@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    data = body["event"]
    question = ""
    if 'blocks' in data and 'elements' in data.get('blocks')[0] and 'elements' in \
            data.get('blocks')[0].get('elements')[0]:
        for e in data.get('blocks')[0].get('elements')[0].get('elements'):
            if 'text' in e and e.get('type', 'unknown') != 'user':
                question += e.get('text')
    if question:
        question = question.strip()
        say(f"Hi <@{data['user']}>! That's a great question. Let me find the answer for you. :hourglass_flowing_sand:",
            channel=data['channel'], thread_ts=data['ts'])
        answer = skill_q_and_a(question)
        say(answer, channel=data['channel'], thread_ts=data['ts'])


# Start your app using Socket Mode
if __name__ == "__main__":
    SocketModeHandler(app, get_slack_app_token(source_config.config_json)).start()
