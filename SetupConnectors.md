## Steps to create UnifyIQ SlackBot

1. These steps should be done by Workplace Administrator for slack
2. Visit https://api.slack.com/apps
3. Click on Create New App Button and Select "From an App Manifest"
   Option ![Create Slack Bot](/resources/images/slack_bot_create.png)
4. Choose the workspace if you are using multiple workspaces
5. Choose YAML
6. Upload the [manifest](unifyiq.yaml)
7. Create the app
8. Click on **"Install to Workspace"** button to install the app. Choose **"Allow"**. 
9. Note the credentials for the slackbot. Copy them temporarily in a scratch pad. 
    1. Client ID
    2. Signing Secret
    3. App Token - Add an app level token by clicking on **"Generate Tokens and Scopes"**.
       Name the token as **"unifyiq"**
       Add scope as `connections:write` scope
       <br>![App Token](/resources/images/app_token.png)<br>
    5. Access Token - Navigate to OAuth & Permissions under Features section of unifyiq app. Copy the token from **"Bot
       User OAuth Token"** ![Bot Auth Token](/resources/images/auth_token.png)
   
10. Update these in the UI when creating slack connector
      ![Admin UI](/resources/images/setup-slack-admin-ui.png)

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
