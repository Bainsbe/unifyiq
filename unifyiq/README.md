# UnifyIQ - Knowledge Assistant

## Pre-requisites

- Python 3.10+
    - https://www.python.org/downloads/macos/ OR https://www.python.org/downloads/windows/
- MySQL
  - Please follow the instructions [here](/schema/database/README.md) to setup MySQL Database
- Slackbot
  - Please follow the instructions [here](/retrieval/slackbot/README.md) doc to setup slackbot
- Docker
  - Please follow the instructions [here](https://docs.docker.com/engine/install/)
- Airbyte
  - Please refer to [Getting Started](https://docs.airbyte.com/quickstart/deploy-airbyte) doc to setup airbyte in your
    machine
    ```
    git clone https://github.com/airbytehq/airbyte.git
    cd airbyte
    ./run-ab-platform.sh
    ```
  - Kill the above process if you want to bring it down
- Milvus
  - Please follow the instructions [here](https://milvus.io/docs/install_standalone-docker.md) to setup Milvus
    ```
      mkdir milvus && cd milvus
      wget https://github.com/milvus-io/milvus/releases/download/v2.2.10/milvus-standalone-docker-compose.yml -O docker-compose.yml
      docker-compose up -d
    ```
  - Run `docker-compose down` to bring it down

## Getting Started

1. Clone the repo to your home directory. In following commands, modify the path to repo path if you are using a
   different path than home directory
    ```
    git clone https://github.com/unifyiq/unifyiq.git
    ```
2. Install the dependencies in [requirements.txt](/unifyiq/requirements.txt)
    ```
   python3 -m venv unifyiq-venv
   cd unifyiq-venv
   source bin/activate
   cd ~/unifyiq/unifyiq
   pip3 install -r requirements.txt
    ```
3. Follow the instruction [here](/unifyiq/fetchers/README.md) to setup slack data source
4. Copy the [config file](/unifyiq/conf/unifyiq.ini) to your home directory and update the values
    ```
    cp ~/unifyiq/unifyiq/conf/unifyiq.ini ~/
    ```
5. Once the slack data is available in `/tmp/airbyte_local/unifyiq_slack`, run the following command to consume the data
    ```
    python3 -m fetchers.update_fetchers
    ```
6. Once the data is consumed, run the following command to index the data.
    ```
    python3 -m core.update_core
    ```
7. Once the data is indexed, run the following command to start the web server
    ```
    python3 -m api.app
    curl -X POST "http://127.0.0.1:8080/get_answer" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "question=what is the status of project skynet?"
    ```
