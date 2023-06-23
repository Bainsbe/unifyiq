# Adapters for Data From External Sources

## UnifyIQ Supported Systems

Our Knowledge Assistant is still learning and growing. As of now, it only supports the following sources and
destinations.

## Airbyte

### Sources

#### Slack

Follow instructions in the airbyte UI to setup a new slack source.

1. Set Join Channels to be ON
2. Set Threads Lookback window to 7 days (Setting it longer might not be very efficient)
3. Set the start date or history of slack you need to index as Start Date

### Destinations

Destinations where airbyte will store the data extracted from Sources.

#### Local JSON

Set the destination as Local JSON

1. Set the Destination name and Destination path as `unifyiq_slack`
2. Output will be stored in `/tmp/airbyte_local/unifyiq_slack` (Behavior In Mac)

### Connections

#### Slack to Local JSON

Set the Connection Configs

1. Set the replication frequency to be Cron and Night Time for your timezone
2. Set the messages and threads streams to be Incremental | append
   ![Slack Connector](/resources/images/slack_airbyte_connector.png)

## Configuring the fetcher

1. Insert the following row to the `unifyiq_configs` table after replacing the values in `[]` with the appropriate
   values
    ```
    INSERT INTO unifyiq_configs(name, connector_platform, connector_type, src_storage_type, src_path, dest_storage_type,
                                dest_path, url_prefix, cron_expr, last_fetched_ts, is_enabled) 
    VALUES('unifyiq_slack', 'AIRBYTE', 'SLACK', 'LOCAL', '/tmp/airbyte_local/unifyiq_slack/', 'LOCAL', '[HOME]/unifyiq/fetchers','https://[WORKSPACE].slack.com/', '0 2 * * *', 0, true);    
    ```

## Adding a new fetcher

1. Setup the source in Airbyte http://localhost:8000
2. Create a new adapter that extends AirbyteAdapter
3. Create the necessary metadata tables in the database and add to (schemas)[/schema/database/]
4. Implement method `parse_jsonl` to parse the json file
    1. Update the metadata
    2. Output the JSON using `BaseAdapter.validate_and_write_json` and make sure the required fields are set
       using `BaseAdapter.set_required_values_in_json` 
