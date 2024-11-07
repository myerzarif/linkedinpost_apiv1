# Ready the environment
virtualenv -p /Users/mahyar/anaconda3/bin/python .venv
source .venv/bin/activate
pip install -r requirements.txt
copy the content of .env.sample to .env file and replace it with valid credentials and values
python3 src/main.py

# Start the app by Docker
docker network create linkedin_apiv1_network
docker volume create --name=linkedin_mongo_volume
cp .env.sample .env (edit .env file)
sudo docker compose up -d --build
Now you should be able to see the doc page: http://localhost:8080/docs