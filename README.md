# S-ProvFlow

Provenance framework for storage and access of data-intensive streaming lineage. It offers a a web API and a range of dedicated visualisation tools. It offers a web API, a range of dedicated vis-ualisation tools and provenance model (S-PROV) based on a specialisation of the W3C-PROV format. 

![alt tag](https://raw.githubusercontent.com/aspinuso/s-provenance/master/resources/template.png)

- A collection of services including a WEB-API (provenance-api) and a front-end GUI (provenance-explorer) allowing acquisition and exploration of provenance data which is produced at a run-time by a computational engine.

![alt tag](https://raw.githubusercontent.com/aspinuso/s-provenance/master/resources/totalv.png)
![alt tag](https://raw.githubusercontent.com/KNMI/s-provenance/master/resources/vis-prov006.png)

- S-ProvFlow manages provenance traces provided by data-intesive systems such has dispel4py and its integration within the WPS (Web Processing Services), implemented with the PyWPS framework, is currently ongoing (https://github.com/KNMI/wps_workflow). 

- S-ProvFlow is the provenance framework integrated within the VERCE Earthquakes Simulation portal (http://portal.verce.eu) and the climate services portal (http://climate4impact.eu).

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
