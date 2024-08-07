FROM --platform=linux/amd64  python:3.9
	 
 WORKDIR /app
 
 RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
 COPY requirements.txt requirements.txt
 RUN pip3 install -r requirements.txt
 
 COPY . .

 CMD [ "python3","-u", "drillout.py"]