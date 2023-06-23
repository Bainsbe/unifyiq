### Steps to create UnifyIQ SlackBot

1. These steps should be done by Workplace Administrator for slack
2. Visit https://api.slack.com/apps
3. Click on Create New App Button and Select "From an App Manifest"
   Option ![Create Slack Bot](/resources/images/slack_bot_create.png)
4. Chose the workspace if you are using multiple workspaces
5. Upload the [manifest](unifyiq.yaml)
6. Create and Install the app to your workplace
7. Note the credentials for the slackbot that you will need for airbyte as well
    1. Client ID
    2. Signing Secret
    3. Access Token - Navigate to OAuth & Permissions under Features section of unifyiq app. Copy the token from "Bot
       User OAuth Token" ![Bot Auth Token](/resources/images/auth_token.png)
8. Update these in ~/unifyiq.ini
