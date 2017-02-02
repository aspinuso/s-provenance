# s-provenance

Provenance framework for data-intensive streaming. It offers a a web API and a range of dedicated visualisation tools. The API exports data in W3C-PROV format. 

- A collection of services including a WEB-API (provenance-api) and a front-end GUI (provenance-explorer) allowing acquisition and exploration of provenance data which is produced at a run-time by a computational engine.
- Currently manages provenance traces provided by data-intesive systems such has dispel4py and WPS (Web Processing Services) services, implemented with the PyWPS framework. This is the provenance framework integrated within the VERCE Earthquakes Simulation portal (http://portal.verce.eu) and the climate services portal (http://climate4impact.eu).

## Requirements and dependencies

### provenance-explorer
- Compile, Maven2 >= v3.2.5
- Apache Tomcat >= v7.x
- Java proxy j2ep v1.0
 
### provenance-api
- twisted >= v16.2.0
- pymongo >= v3.4.0
- Mongodb >= v2.4.4

