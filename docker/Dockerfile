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
	mongodb

# python requirements
RUN pip install --no-cache-dir -r requirements.txt

#RUN sudo service mongod start
CMD["/etc/init.d/mongodb","start"] # issue?


# /prov/s-provenance-master/provenance-api/src/prov-services/
# ENTRYPOINT[start_sprovapi_flask_gunicorn.sh]
# download test data...


#
# docker run -it --rm tomcat:9.0 
# docker build . -t prov:dockerfile
# docker images
# docker run prov
# docker exec -it 36c1221d56be bash
# 

