# image tomcat on debian
FROM tomcat:9.0

RUN mkdir -p /prov/
WORKDIR /prov/

# s-prov download from git
RUN curl -L -O https://github.com/KNMI/s-provenance/archive/master.zip 
RUN unzip master.zip

# linux requiremnets
COPY requirements.txt /prov/
RUN apt-get update && apt-get install -y \
	procps \
	python \
	python-pip \
	vim \
	mongodb

# python requirements
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8082

# to run mongo
# example at /prov/s-provenance-master/provenance-api/resources/mongo-bash
# CMD["/etc/init.d/mongodb","start"] # issue?
# RUN /etc/init.d/mongodb start # as demon
RUN /bin/mongod --dbpath /tmp/ --logpath /tmp/mongo.log --auth &



# WORKDIR /prov/s-provenance-master/provenance-api/src/prov-services/
# ENTRYPOINT["start_flask_gunicorn.sh"]
# download test data...


#
# docker run -it --rm tomcat:9.0 
# docker build . -t prov
# docker images
# docker run -it prov
# docker exec -it 36c1221d56be bash
# 

