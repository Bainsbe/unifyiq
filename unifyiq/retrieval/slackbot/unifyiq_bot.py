from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from api.assistant import skill_q_and_a
from utils.configs import get_slack_bot_token, get_slack_app_token

# Initialize your app with your bot token
app = App(token=get_slack_bot_token())


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
    answer = skill_q_and_a(question)
    say(answer, channel=data['channel'], thread_ts=data['ts'])


# Start your app using Socket Mode
if __name__ == "__main__":
    SocketModeHandler(app, get_slack_app_token()).start()
