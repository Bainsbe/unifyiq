# Adapters for Data From External Sources

## UnifyIQ Supported Systems

Our Knowledge Assistant is still learning and growing. As of now, it only supports the following sources and
destinations.

### Sources

1. Slack
    1. Follow the instructions [here](/unifyiq/retrieval/slackbot/README.md) to setup the SlackBot and get the required
       credentials
2. Confluence Wiki
    1. Visit https://id.atlassian.com/manage-profile/security/api-tokens
    2. Create a new API token
    3. Use the email address, site name and the API token to configure the Confluence adapter in unifyiq.ini

### Destinations

1. Local JSON

## Adding a new fetcher

1. Explore the API access to the data source
    1. If the source is already supported by LangChain, then use the LangChain library
    2. If not, then use the source API directly
2. Create a new adapter that extends BaseAdapter
3. Create the necessary metadata tables in the database and add to (schemas)[/schema/database/]
4. Implement all abstract methods to extract metadata and data from the source
    1. load_metadata_from_db
        1. Extract the metadata from database to determine the changes
        2. e.g. Slack Channel Information, Slack Channel membership etc.
    2. fetch_and_save_raw_data
        1. Fetch the raw data from the source and save it to the local storage.
        2. Use `BaseAdapter.start_ts` and `BaseAdapter.end_ts` to determine the time range for incremental fetch
            1. Process data that satisfy `BaseAdapter.start_ts` < `ts` < `BaseAdapter.end_ts`
        3. Use `BaseAdapter.set_required_values_in_json` to make sure the required fields are set
        4. Use `BaseAdapter.validate_and_write_json` to write to the appropriate paths. This will fail if the required
           fields are not set
        5. e.g. Slack Channel messages
    3. save_metadata_to_db
        1. Save the metadata to the database
        2. e.g. Slack Channel Information, Slack Channel membership etc.
5. Add the api layer to the adapter if we need to expose the metadata in UI

## Configuring the fetcher

1. Insert the following row to the `unifyiq_configs` table after
2. Replace the values in `[]` with the appropriate values
    1. WORKSPACE - Slack Workspace

 ~~~~sql
 INSERT INTO unifyiq_configs(name, connector_type, url_prefix, cron_expr, start_ts, last_fetched_ts, is_enabled)
        VALUES('unifyiq_slack', 'SLACK','https://[WORKSPACE].slack.com/', '0 2 * * *', 1672560000, 0, true);
 INSERT INTO unifyiq_configs(name, connector_type, url_prefix, cron_expr, start_ts, last_fetched_ts, is_enabled)
        VALUES('unifyiq_confluence', 'CONFLUENCE','https://[WORKSPACE].atlassian.net/', '0 2 * * *', 1672560000, 0, true);   
 ~~~~
