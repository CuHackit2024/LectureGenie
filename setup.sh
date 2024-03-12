sudo apt update -y
sudo apt install python3-pip -y
sudo pip install poetry

poetry export -f requirements.txt --output requirements.txt
sudo pip install -r requirements.txt
sudo pip install -U openai-whisper
sudo apt install ffmpeg -y