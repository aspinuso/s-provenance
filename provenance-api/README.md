s-prov
======
**Version:** v1

### /data
---
##### ***GET***
**Description:** The data is selected by specifying a query string. Query parameters allow to search by attribution to a component or to an implementation, generation by a workflow execution and by combining more metadata and parameters terms with their min and max valuesranges. Mode of the search can also be indicated (mode ::= (OR | AND). It will apply to the search upon metadata and parameters values-ranges

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| usernames | query | csv list of users the Workflows Executons are associated with | No | string |
| terms | query | csv list of metadata or parameter terms. These relate positionally to the maxvalues and the minvalues | No | string |
| functionNames | query | csv list of functions the Data was generated with | No | string |
| wasAttributedTo | query | csv list of Component or Component Instances involved in the generation of the Data | No | string |
| minvalues | query | csv list of metadata or parameters minvalues. These relate positionally to the terms and the minvalues | No | string |
| rformat | query | unimplemented: format of the response payload (json,json-ld) | No | string |
| start | query | index of the starting item | Yes | integer |
| limit | query | max number of items expected | Yes | integer |
| maxvalues | query | csv list of metadata or parameters maxvalues. These relate positionally to the terms and the minvalues | No | string |
| formats | query | csv list of data formats (eg. mime-types) | No | string |
| types | query | csv list of data types | No | string |
| wasGeneratedBy | query | the id of the Invocation that generated the Data | No | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /data/filterOnAncestor
---
##### ***POST***
**Description:** Filter a list of data ids based on the existence of at least one ancestor in their data dependency graph, according to a list of metadata terms and their min and max values-ranges. Maximum depth level and mode of the search can also be indicated (mode ::= (OR | AND)

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body |  | No | object |

**Responses**

| Code | Description |
| ---- | ----------- |

### /data/{data_id}
---
##### ***GET***
**Description:** Extract Data and their DataGranules by the Data id

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data_id | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /data/{data_id}/derivedData
---
##### ***GET***
**Description:** Starting from a specific data entity of the data dependency is possible to navigate through the derived data or backwards across the element's data dependencies. The number of traversal steps is provided as a parameter (level).

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| level | query | level of depth in the data derivation graph, starting from the current Data | Yes | string |
| data_id | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /data/{data_id}/export
---
##### ***GET***
**Description:** Export of provenance information PROV-XML or RDF format. The S-PROV information returned covers the whole workflow execution or is restricted to a single data element. In the latter case, the graph is returned by following the derivations within and across runs. A level parameter allows to indicate the depth of the resulting trace

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| format | query | export format of the PROV document returned | No | string |
| rdfout | query | export rdf format of the PROV document returned | No | string |
| creator | query | the name of the user requesting the export | No | string |
| level | query | level of depth in the data derivation graph, starting from the current Data | Yes | string |
| data_id | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /data/{data_id}/wasDerivedFrom
---
##### ***GET***
**Description:** Starting from a specific data entity of the data dependency is possible to navigate through the derived data or backwards across the element's data dependencies. The number of traversal steps is provided as a parameter (level).

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| level | query | level of depth in the data derivation graph, starting from the current Data | Yes | string |
| data_id | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /instances/{instid}
---
##### ***GET***
**Description:** Extract details about a single instance or component by specifying its id. The returning document will indicate the changes that occurred, reporting the first invocation affected. It support the specification of a list of runIds the instance was wasAssociateFor, considering that the same instance could be used across multiple runs

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| start | query | index of the starting item | Yes | integer |
| limit | query | max number of items expected | Yes | integer |
| wasAssociateFor | query | cvs list of runIds the instance was wasAssociateFor (when more instances are reused in multiple workflow executions) | No | string |
| instid | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /invocations/{invocid}
---
##### ***GET***
**Description:** Extract details about a single invocation by specifying its id

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| invocid | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /summaries/collaborative
---
##### ***GET***
**Description:** Extract information about the reuse and exchange of data between workflow executions based on terms' valuesranges and a group of users. The API method allows for inclusive or exclusive (mode ::= (OR j AND) queries on the terms' values. As above, additional details, such as running infrastructure, type and name of the workflow can be selectively extracted by assigning these properties to a groupBy parameter. This will support the generation of grouped views

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| wasAssociatedWith | query | csv lis of Components involved in the Workflow Executions | No | string |
| usernames | query | csv list of users the Workflows Executons are associated with | No | string |
| terms | query | csv list of metadata or parameter terms. These relate positionally to the maxvalues and the minvalues | No | string |
| functionNames | query | csv list of functions that are executed by at least one workflow's components | No | string |
| level | query | level of depth in the data derivation graph, starting from the current Data | Yes | string |
| minvalues | query | csv list of metadata or parameters minvalues. These relate positionally to the terms and the minvalues | No | string |
| rformat | query | unimplemented: format of the response payload (json,json-ld) | No | string |
| maxvalues | query | csv list of metadata or parameters maxvalues. These relate positionally to the terms and the minvalues | No | string |
| formats | query | csv list of data formats (eg. mime-types) | No | string |
| clusters | query | csv list of clusters that describe and group one or more workflow's component | No | string |
| groupby | query | express the grouping of the returned data | No | string |
| types | query |  | No | string |
| mode | query | execution mode of the workflow in case it support different kind of concrete mappings (eg. mpi, simple, multiprocess, etc.. | No | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /summaries/workflowexecution
---
##### ***GET***
**Description:** Produce a detailed overview of the distribution of the computation, reporting the size of data movements between the workflow components, their instances or invocations across worker nodes, depending on the specified granularity level. Additional information, such as process pid, worker, instance or component of the workflow (depending on the level of granularity) can be selectively extracted by assigning these properties to a groupBy parameter. This will support the generation of grouped views

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| level | query | level of depth in the data derivation graph, starting from the current Data | Yes | string |
| mintime | query | minimum start time of the Invocation | No | string |
| groupby | query | express the grouping of the returned data | No | string |
| runId | query | the id of the run to be analysed | No | string |
| maxtime | query | maximum start time of the Invocation | No | string |
| maxidx | query | maximum iteration index of an Invocation | No | integer |
| minidx | query | minimum iteration index of an Invocation | No | integer |

**Responses**

| Code | Description |
| ---- | ----------- |

### /terms
---
##### ***GET***
**Description:** Return a list of discoverable metadata terms based on their appearance for a list of runIds, usernames, or for the whole provenance archive. Terms are returned indicating their type (when consistently used), min and max values and their number occurrences within the scope of the search

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| aggregationLevel | query | set whether the terms need to be aggreagated by runId, username or across the whole collection (all) | No | string |
| usernames | query | csv list of usernames | No | string |
| runIds | query | csv list of run ids | No | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /workflowexecutions
---
##### ***GET***
**Description:** Extract documents from the bundle collection according to a query string which may include usernames, type of the workflow, the components the run wasAssociatedWith and their implementations. Data results' metadata and parameters can also be queried by specifying the terms and their min and max values-ranges and data formats. Mode of the search can also be indicated (mode ::= (OR j AND). It will apply to the search upon metadata and parameters values of each run

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| wasAssociatedWith | query | csv lis of Components involved in the Workflow Executions | No | string |
| usernames | query | csv list of users the Workflows Executons are associated with | No | string |
| terms | query | csv list of metadata or parameter terms. These relate positionally to the maxvalues and the minvalues | No | string |
| functionNames | query | csv list of functions that are executed by at least one workflow's components | No | string |
| minvalues | query | csv list of metadata or parameters minvalues. These relate positionally to the terms and the minvalues | No | string |
| rformat | query | unimplemented: format of the response payload (json,json-ld) | No | string |
| start | query | index of the starting item | Yes | integer |
| limit | query | max number of items expected | Yes | integer |
| maxvalues | query | csv list of metadata or parameters maxvalues. These relate positionally to the terms and the minvalues | No | string |
| formats | query | csv list of data formats (eg. mime-types) | No | string |
| clusters | query | csv list of clusters that describe and group one or more workflow's component | No | string |
| types | query |  | No | string |
| mode | query | execution mode of the workflow in case it support different kind of concrete mappings (eg. mpi, simple, multiprocess, etc.. | No | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /workflowexecutions/insert
---
##### ***POST***
**Description:** Bulk insert of bundle or lineage documents in JSON format. These must be provided as encoded stirng in a POST request

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body |  | No | object |

**Responses**

| Code | Description |
| ---- | ----------- |

### /workflowexecutions/{run_id}/export
---
##### ***GET***
**Description:** Export of provenance information PROV-XML or RDF format. The S-PROV information returned covers the whole workflow execution or is restricted to a single data element. In the latter case, the graph is returned by following the derivations within and across runs. A level parameter allows to indicate the depth of the resulting trace

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| rdfout | query | export rdf format of the PROV document returned | No | string |
| creator | query | the name of the user requesting the export | No | string |
| format | query | export format of the PROV document returned | No | string |
| run_id | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /workflowexecutions/{runid}
---
##### ***DELETE***
**Description:** Extract documents from the bundle collection by the runid of a WFExecution. The method will return input data and infomation about the components and the libraries used for the specific run

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| runid | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

##### ***GET***
**Description:** Extract documents from the bundle collection by the runid of a WFExecution. The method will return input data and infomation about the components and the libraries used for the specific run

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| runid | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /workflowexecutions/{runid}/delete
---
##### ***POST***
**Description:** Delete a workflow execution trace, including its bundle and all its lineage documents

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| runid | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /workflowexecutions/{runid}/edit
---
##### ***POST***
**Description:** Update of the description of a workflow execution. Users can improve this information in free-tex

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body |  | No | object |
| runid | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

### /workflowexecutions/{runid}/showactivity
---
##### ***GET***
**Description:** Extract detailed information related to the activity related to a WFExecution (id). The result-set can be grouped by invocations, instances or components (parameter level) and shows progress, anomalies (such as exceptions or systems' and users messages), occurrence of changes and the rapid availability of accessible data bearing intermediate results. This method can also be used for runtime monitoring

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| start | query | index of the starting item | Yes | integer |
| limit | query | max number of items expected | Yes | integer |
| level | query | level of aggregation of the monitoring information (component, instance, invocation, cluster) | No | string |
| runid | path |  | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |

