# image knmi
FROM ubuntu

LABEL "KNMI PROVENANCE STORE CONTAINER"

RUN mkdir -p /prov/
WORKDIR /prov/

# linux tools
RUN apt-get update && apt-get install -y \
	curl  \
	unzip \
	procps \
	python \
	python-pip \
	vim


# couple this file to a seperate mongo instance, pull docker mongo 3.4
# see docker-compose.yml

# s-prov download from git
RUN curl -L -O https://github.com/aspinuso/s-provenance/archive/master.zip 
RUN unzip master.zip

# python requirements
COPY requirements.txt /prov/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8082
EXPOSE 27017

# provenance repo
WORKDIR /prov/s-provenance-master/provenance-api/src/prov-services/

ENV CLIMEXPFORTRAN='../Fortran'
ENV SPROV_DB=sprov-db

# added mongo features...

# RUN echo 'mongo --eval "var dbName = '$SPROV_DB'"  /prov/s-provenance-master/provenance-api/resources/ensure_indexes.js' >> docker_entry.sh
# crontab map reduce
# RUN mongo --eval "var dbName = '$SPROV_DB'"  /prov/s-provenance-master/provenance-api/resources/lineage_map_reduce.js

# RUN curl localhost:27017

ENTRYPOINT sh -p ./start_flask_gunicorn_docker.sh

CMD bash ./start_flask_gunicorn_docker.sh



#
# docker build docker/ --rm -t prov
# docker rmi $(docker images -f "dangling=true" -q)
# docker run -it -d -p 8083:8082 prov
# docker run -it -d -p 8083:8082 -v /nobackup/users/mihajlov/data:/prov/data prov
# docker run -it -d --name=sprov -p 8083:8082 -v /nobackup/users/mihajlov/data:/prov/data prov 
# docker run -it -d -p 8083:8082 prov
# docker run -it -d -p 8083:8082 /tmp:/prov/data prov
# docker exec -it docker_name bash
# docker logs -f docker_name
# 


