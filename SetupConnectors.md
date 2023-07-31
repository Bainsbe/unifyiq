### Steps to setup SlackBot

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
   
10. Go to Admin UI, Add a connector, Choose Slack and enter the above values.
      1. Make sure to use your workspace specific slack url in URL Prefix: https://[WORKSPACE].slack.com/
      2. Set the start date to be the date from which historical data needs to be ingested.
      3. See example values here:
      ![Admin UI](/resources/images/setup_setup_image.png)


### Steps to setup Confluence Wiki
1. Create a new headless user in Confluence (e.g. unifyiq)
2. Visit https://id.atlassian.com/manage-profile/security/api-tokens
3. Create a new API token
4. Use the email address, site name and the API token to configure the Confluence adapter in admin UI
5. URL Prefix: https://[WORKSPACE].atlassian.net/

