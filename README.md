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

# mongo express
http://localhost:8081/

# deployment on azure
az acr login --name cgcontainerregistry
docker tag linkedin_apiv1 cgcontainerregistry.azurecr.io/generation_apiv1:latest
docker push cgcontainerregistry.azurecr.io/generation_apiv1:latest
az acr repository list --name cgcontainerregistry --output table

# Build and push on mac
docker buildx build --platform linux/amd64 -t cgcontainerregistry.azurecr.io/generation_apiv1:latest .
TEST: docker run -p 5050:5050 cgcontainerregistry.azurecr.io/linkedincgapi_cg_apiv1:latest
az acr login --name cgcontainerregistry
docker push cgcontainerregistry.azurecr.io/generation_apiv1:latest