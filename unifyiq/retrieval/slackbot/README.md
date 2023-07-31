## Steps to create UnifyIQ SlackBot

1. These steps should be done by Workplace Administrator for slack
2. Visit https://api.slack.com/apps
3. Click on Create New App Button and Select "From an App Manifest"
   Option ![Create Slack Bot](/resources/images/slack_bot_create.png)
4. Choose the workspace if you are using multiple workspaces
5. Choose YAML
6. Upload the [manifest](unifyiq.yaml)
7. Create and Install the app to your workplace
8. Note the credentials for the slackbot
    1. Client ID
    2. Signing Secret
    3. Access Token - Navigate to OAuth & Permissions under Features section of unifyiq app. Copy the token from "Bot
       User OAuth Token" ![Bot Auth Token](/resources/images/auth_token.png)
    4. App Token - Navigate to Basic Information under Settings section of unifyiq app. Add an app level token with
       `connections:write` scope
       <br>![App Token](/resources/images/app_token.png)<br>
9. Update these in the UI when creating slack connector

## Steps to interact with UnifyIQ SlackBot (Needed only for dev env. in laptop)

1. Run the following command to start the slack SocketMode server
    ```commandline
    python3 -m retrieval.slackbot.unifyiq_bot
    ```
2. For Mac, If there are any SSL errors that's preventing the server from starting, run the following command
    ```commandline
    /Applications/Python\ 3.10/Install\ Certificates.command
    ```
2. In any channel, type `@unifyiq <question>` to get the list of commands
    1. e.g. ```@unifyiq what is the status of project skynet```
