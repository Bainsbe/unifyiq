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
- This instance can be used for Milvus, UnifyIQ, and the database. If the load is too high, you can split them into separate instances.

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
- Run the playbook
  - Playbook uses mysql credentials from the config file, so above step is required 
  - Modify the `inventory` with correct IP address (Private IP) and key file path
  - `ansible-playbook playbook.yml`
  - This will bring up database, milvus and unifyiq services