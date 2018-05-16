FROM tomcat

LABEL "TITLE"="Docker file for sprovflow-viewer"
LABEL "MAINTAINER"="prov@knmi.nl"

RUN apt-get update && apt-get install -y maven curl less vim 


# clone s-prov
RUN mkdir -p /prov/
WORKDIR /prov/
RUN curl -L -O https://github.com/aspinuso/s-provenance/archive/master.zip 
RUN unzip master.zip
RUN rm master.zip

# compile viewer.war
WORKDIR /prov/s-provenance-master/sprovflow-viewer

RUN mvn compile war:war
		
RUN cp ./target/sprovflow-viewer.war /usr/local/tomcat/webapps

RUN cp /prov/s-provenance-master/resources/j2ep-1.0.war /usr/local/tomcat/webapps


#CMD cp /prov/s-provenance-master/resources/data.xml /usr/local/tomcat/webapps/j2ep-1.0/WEB-INF/config/data.xml 
#CMD touch /usr/local/tomcat/webapps/j2ep-1.0/WEB-INF/web.xml

## touch /prov/s-provenance-master/resources/data.xml
## RUN /usr/local/tomcat/bin/shutdown.sh
 

# docker run -it -p 9000:8080 viewer


