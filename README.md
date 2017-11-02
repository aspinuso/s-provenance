# S-ProvFlow

Provenance framework for storage and access of data-intensive streaming lineage. It offers a a web API and a range of dedicated visualisation tools and a provenance model (S-PROV) which utilises and extends PROV and ProvONE models. S-PROV addresses aspects of mapping between logical representation and concrete implementation of a workflow until its enactment onto a target computational resource.  The model captures aspects associated with the distribution of the computation, volatile and materialised data-flow and the management of the internal state of each concrete process. Moreover, it captures changes occurring to the workflow at runtime, especially in support of dynamic steering.

![alt tag](https://raw.githubusercontent.com/aspinuso/s-provenance/master/resources/template.png)

- A collection of services including a WEB-API (provenance-api) and a front-end GUI (provenance-explorer) allowing acquisition and exploration of provenance data which is produced at a run-time by a computational engine. Below a schematic representation of the architecture and interaction with external resources, followed by screenshots of the interactive tools.

![alt tag](https://raw.githubusercontent.com/aspinuso/s-provenance/master/resources/sprovflowpnf.png)
![alt tag](https://raw.githubusercontent.com/aspinuso/s-provenance/master/resources/totalv.png)
![alt tag](https://raw.githubusercontent.com/KNMI/s-provenance/master/resources/vis-prov006.png)

- S-ProvFlow manages provenance traces provided by data-intesive systems such has dispel4py and its integration within the WPS (Web Processing Services), implemented with the PyWPS framework, is currently ongoing (https://github.com/KNMI/wps_workflow). 

- S-ProvFlow is the provenance framework integrated within the VERCE Earthquakes Simulation portal (http://portal.verce.eu) and the climate services portal (http://climate4impact.eu).

#### Dockerization

The s-prov project can be deployed using docker technology. The project is split into a store and explorer instances.  The explorer is currently set to connect via the docker bridge to a local instance of the store. Changes to the docker file are required if the explorer is remote.
The store instance is deployable via docker-compose, the mongo db instance is split from the store services api. The store service can also be deployed independently so as to be attached to an existing mongo db. 

s-prov store,
  see **docker/store/docker-compose.yml**
```
  $ cd docker/store/
  $ docker-compose up --build 
```
s-prov viewer
```
   $ docker build docker/viewer/ -t explorer 
   $ docker run -it -p9000:8080 explorer 
```   



## Requirements and dependencies

### provenance-explorer
- Compile, Maven2 >= v3.2.5
- Apache Tomcat >= v7.x
- Java proxy j2ep v1.0
 
### provenance-api
- twisted >= v16.2.0 (deprecated)
- gunicorn >= 19.7.1 (or any WSGI webserver)
- flask >= v0.12.1
- pymongo >= v3.4.0
- Mongodb >= v2.4.4

### Related Projects

- WPS-WORKFLOW: https://github.com/KNMI/wps_workflow
- dispel4py: https://github.com/dispel4py/dispel4py
- VERCE: https://github.com/KNMI/VERCE
