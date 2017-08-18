# image knmi
FROM debian

RUN mkdir -p /prov/
WORKDIR /prov/

# linux tools
RUN apt-get update && apt-get install -y \
	curl  \
	unzip \
	procps \
	python \
	python-pip \
	vim \
	mongodb

# s-prov download from git
RUN curl -L -O https://github.com/andrejsim/s-provenance/archive/master.zip 
RUN unzip master.zip

# python requirements
COPY requirements.txt /prov/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8082

# provenance repo
WORKDIR /prov/s-provenance-master/provenance-api/src/prov-services/


# docker start file
RUN echo './start_flask_gunicorn_docker.sh' >> docker_entry.sh
RUN echo 'mongod --logpath /prov/mongo.log --dbpath /prov/ --auth' >> docker_entry.sh


RUN chmod a+x docker_entry.sh

ENTRYPOINT bash docker_entry.sh

#
# docker build docker/ --rm -t prov
# docker rmi $(docker images -f "dangling=true" -q)
# docker run -it -p 8082:8082 prov &
# docker run -it -d -p 8082:8082 prov
# docker exec -it 36c1221d56be bash
# 


