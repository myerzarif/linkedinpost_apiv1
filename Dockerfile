FROM python:3.11

WORKDIR /linkedin_apiv1

RUN apt-get update

COPY ./requirements.txt /linkedin_apiv1/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 -m pip install -U pip

COPY . .

ENTRYPOINT ["python3" , "src/main.py"]