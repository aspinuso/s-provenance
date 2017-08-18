# image knmi
FROM debian

# image tomcat on debian
#FROM tomcat:9.0

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
RUN curl -L -O https://github.com/aspinuso/s-provenance/archive/master.zip 
RUN unzip master.zip

# python requirements
COPY requirements.txt /prov/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8082

# to run mongo
# example at /prov/s-provenance-master/provenance-api/resources/mongo-bash
# CMD["/etc/init.d/mongodb","start"] # issue?
# RUN /etc/init.d/mongodb start # as demon
# RUN /bin/mongod --dbpath /prov/data/ --logpath /tmp/mongo.log --auth &

# provenance repo
WORKDIR /prov/s-provenance-master/provenance-api/src/prov-services/

# docker start file
RUN echo '/bin/mongod --dbpath /prov/ --logpath /prov/mongo.log --auth &' >> dstart.sh
RUN echo './start_flask_gunicorn.sh' >> dstart.sh
RUN chmod a+x dstart.sh

#ENTRYPOINT bash
#CMD ./dstart.sh

CMD bash

#
# docker build . -t prov
# docker images
# 
# docker exec -it 36c1221d56be bash
# 

