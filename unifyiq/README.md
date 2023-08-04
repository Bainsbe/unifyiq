# Dev Setup

### Install Pre-requisite

- Python 3.10+
    - https://www.python.org/downloads/macos/ OR https://www.python.org/downloads/windows/
- MySQL
    - Please follow the instructions [here](/schema/database/README.md) to setup MySQL Database. Note that after any schema change, DB needs to be [rebuilt](/schema/database/README.md#build-database-run-this-whenever-schema-changes).

### Install source code and Dependencies

1. Clone the repo to your home directory. In following commands, modify the path to repo path if you are using a
   different path than home directory
    ```commandline
    git clone https://github.com/unifyiq/unifyiq.git
    ```
2. Install the dependencies in [requirements.txt](/unifyiq/requirements.txt)
    ```commandline
   python3 -m venv unifyiq-venv
   cd unifyiq-venv
   source bin/activate
   cd ~/unifyiq/unifyiq
   pip3 install -r requirements.txt
    ```
### Run API Server

1. Run the following command to start the API server
    ```commandline
    python3 -m api.app

2. Test the API using this
    curl -X POST "http://localhost:8080/get_answer" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "question=what is the status of project skynet?"
    ```

### Setup and Run Admin UI

Follow the instructions [here](/unifyiq/ui/README.md)

### Configure Connectors

Follow the instruction [here](/SetupConnectors.md) to setup data sources

### Install Vector DB 

- Docker
    - Please follow the instructions [here](https://docs.docker.com/engine/install/)
    - Launch the Docker Desktop application for command line tools to work
- Milvus
    - Please follow the instructions [here](https://milvus.io/docs/install_standalone-docker.md) to setup Milvus
      ```commandline
        mkdir milvus && cd milvus
        brew install wget
        wget https://github.com/milvus-io/milvus/releases/download/v2.2.10/milvus-standalone-docker-compose.yml -O docker-compose.yml
        docker-compose up -d
      ```
    - Run `docker-compose down` to bring it down


### Run Data Fetcher and Indexer

1. Copy the [config file](/unifyiq/conf/unifyiq.ini) to your home directory
   ```commandline
   cp ~/unifyiq/unifyiq/conf/unifyiq.ini ~/
   ```
    1. In ~/unifyiq.ini do the required changes.
    2. Update the configs in UnifyIQ section according to your needs

2. Run the following command to consume the data
    ```commandline
    python3 -m fetchers.update_fetchers
    ```
3. Once the data is consumed, run the following command to index the data.
    ```commandline
    python3 -m core.update_core
    ```

### Run Slackbot Server to answer questions from bot added to Slack

1. To start the slackbot, run the following command
    ```commandline
    python3 -m retrieval.slackbot.unifyiq_bot
    ```
    1. In any channel, type `@unifyiq <question>` to get the list of commands
        1. e.g. ```@unifyiq what is the status of project skynet```
    2. For Mac, If there are any SSL errors that's preventing the server from starting, run the following command
    ```commandline
    /Applications/Python\ 3.10/Install\ Certificates.command
    ```
