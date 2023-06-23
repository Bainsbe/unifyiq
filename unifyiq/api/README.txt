-- check if you have python3
python3 --version

-- If python version is lower than 3.10.10, then
-- Install python 3.10.10 (or higher) from
-- https://www.python.org/downloads/macos/ OR https://www.python.org/downloads/windows/

-- Install flask and dependencies
pip3 install Flask
pip3 install pinecone-client
pip3 install openai

-- add keys to ~/.zshrc or ~/.bashrc
-- export OPENAI_API_KEY=...
-- export PINECONE_API_KEY=...
-- source the file

-- Use PyCharm as IDE (https://www.jetbrains.com/pycharm/download/)
-- Create a new project with api folder as root

-- run rest service
python3 app.py

-- example POST request
curl -X POST "http://127.0.0.1:8080/get_answer" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "question=ssh vs password"
