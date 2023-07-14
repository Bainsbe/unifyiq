## AWS Setup

### Controller

- Launch an EC2 instance with the following settings:
    - AMI: Ubuntu Server 18.04 LTS (HVM), SSD Volume Type
    - Instance Type: t2.micro
    - Security Group: SSH, HTTP, HTTPS
    - Key Pair: Create a new key pair and download it

### Milvus / UnifyIQ / DB

- Launch an EC2 instance with the following settings:
    - AMI: Ubuntu Server 18.04 LTS (HVM), SSD Volume Type
    - Instance Type: t2.large
    - Security Group: SSH, HTTP, HTTPS
        - For added security, you can restrict the source IP to the controller's IP for SSH
    - Key Pair: Use the same key pair as the controller
    - Copy the private IP of the instance
- This instance can be used for Milvus, UnifyIQ, and the database. If the load is too high, you can split them into
  separate instances.

### Setup

- SSH into the controller instance
- Install Ansible
    - `sudo apt update`
    - `sudo apt install python3-pip`
    - `python3 -m pip install --user ansible`
- Clone this repository
    - `git clone https://github.com/unifyiq/unifyiq.git`
- Navigate to the ansible directory in the repository
    - `cd unifyiq/playbooks`
- Copy the config file to the home directory
    - `cp ~/unifyiq/conf/unifyiq.ini ~/`
    - Update the values in the config file with required mysql, slackbot and openai credentials
    - Update the milvus host with the private IP of the milvus instance if its a different machine
- Run the playbook
    - Playbook uses mysql credentials from the config file, so above step is required
    - Modify the `inventory` with correct IP address (Private IP) and key file path
    - `ansible-playbook playbook.yml`
    - This will bring up database, milvus and unifyiq services
- Launch the Jobs
    - SSH to MySQL instance
        - This will not be necessary once the UI is ready
        - Follow the steps in [Configure your fetchers](/unifyiq/fetchers/README.md#configuring-the-fetcher) to setup
          the fetchers
    - SSH to UnifyIQ instance
        - Run the following commands
      ```commandline
      cd ~/unifyiq/unifyiq
      nohup python3 unifyiq_update_job.py >> /tmp/unifyiq_update_job.log &
      nohup python3 -m api.app >> /tmp/unifyiq_api_job.log &
      nohup python3 -m retrieval.slackbot.unifyiq_bot >> /tmp/unifyiq_slackbot.log &
      ```