FROM tomcat

LABEL "Docker file for provenance-explorer"

MAINTAINER prov@knmi.nl

RUN apt-get update && apt-get install -y maven curl

# clone s-prov
RUN mkdir -p /prov/
WORKDIR /prov/
RUN curl -L -O https://github.com/aspinuso/s-provenance/archive/master.zip 
RUN unzip master.zip
RUN rm master.zip

# compile viewer.war
WORKDIR /prov/s-provenance-master/provenance-explorer

RUN mvn compile war:war

#COPY ./target/provenance-explorer.war /usr/local/tomcat/webapps

# docker run -it -p 9000:8080 explorer
