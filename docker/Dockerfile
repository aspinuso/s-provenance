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

# mongodb-org v3.4 required
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
RUN echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.4.list
RUN apt-get update && apt-get install -y mongodb-org

# s-prov download from git
RUN curl -L -O https://github.com/aspinuso/s-provenance/archive/master.zip 
RUN unzip master.zip

# python requirements
COPY requirements.txt /prov/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8082

# provenance repo
WORKDIR /prov/s-provenance-master/provenance-api/src/prov-services/

# VOLUME /prov/data/ /data/ # check syntax...

# docker start file
RUN echo './start_flask_gunicorn_docker.sh' >> docker_entry.sh
RUN echo 'mongod --logpath /prov/mongo.log --dbpath /prov/' >> docker_entry.sh
#RUN echo 'mongod --logpath /prov/mongo.log --dbpath /prov/ --auth' >> docker_entry.sh

ENV CLIMEXPFORTRAN='../Fortran'
ENV SPROV_DB=sprov-db

RUN echo 'mongo --eval "var dbName = '$SPROV_DB'"  /prov/s-provenance-master/provenance-api/resources/ensure_indexes.js' >> docker_entry.sh

# crontab map reduce
# import data ?

RUN chmod a+x docker_entry.sh

#ENTRYPOINT bash docker_entry.sh
CMD bash docker_entry.sh

#
# docker build docker/ --rm -t prov
# docker rmi $(docker images -f "dangling=true" -q)
# docker run -it -d -p 8082:8082 prov
# docker exec -it docker_name bash
# docker logs -f docker_name
# 


