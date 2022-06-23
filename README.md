# ens-domains-availability-checker
To build project run: 
`docker build -t domains-cheker:latest . --build-arg BOT_TOKEN=token --build-arg DB_PASSWORD=password`
To start container run:
`docker run -t -d domains-cheker`