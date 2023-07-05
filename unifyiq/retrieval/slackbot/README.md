## Steps to create UnifyIQ SlackBot

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
    4. App Token - Navigate to Basic Information under Settings section of unifyiq app. Add an app level token with
       `connections:write` scope
       <br>![App Token](/resources/images/app_token.png)<br>
8. Update these in ~/unifyiq.ini

## Steps to interact with UnifyIQ SlackBot

1. Run the following command to start the slack SocketMode server
    ```commandline
    python3 -m retrieval.slackbot.unifyiq_bot
    ```
2. In any channel, type `@unifyiq <question>` to get the list of commands
    1. e.g. ```@unifyiq what is the status of project skynet```
