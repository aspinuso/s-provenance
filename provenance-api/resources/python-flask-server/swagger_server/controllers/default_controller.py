import connexion
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

import flask_raas

def activities_run_id_get(runId):
    """
    def activitiesHandler(runId):
    
    :param runId: runId
    :type runId: str

    :rtype: None
    """
    return 'do some magic!'


def components_compid_get(compid):
    """
    def getComponentDetails(compid):
    
    :param compid: compid
    :type compid: str

    :rtype: None
    """
    return 'do some magic!'


def data_data_id_export_get(data_id):
    """
    def _exportDataProvenance(data_id):
    
    :param data_id: data_id
    :type data_id: str

    :rtype: None
    """
    return 'do some magic!'


def data_get():
    """
    def getData():
    

    :rtype: None
    """
    return 'do some magic!'


def data_granule_terms_get():
    """
    def getDataGranuleTerms():
    

    :rtype: None
    """
    return 'do some magic!'


def derived_data_id_get(id):
    """
    def derivedData(id):
    
    :param id: id
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def entities_method_get(method):
    """
    def getEntitiesByMethod(method):
    
    :param method: method
    :type method: str

    :rtype: None
    """
    return 'do some magic!'


def entities_method_post(method):
    """
    entities_method_post
    
    :param method: method
    :type method: str

    :rtype: None
    """
    return 'do some magic!'


def instances_instid_get(instid):
    """
    def getInstanceDetails(instid): 
    
    :param instid: instid
    :type instid: str

    :rtype: None
    """
    return 'do some magic!'


def invocations_invocid_get(invocid):
    """
    def getInvocationDetails(invocid):
    
    :param invocid: invocid
    :type invocid: str

    :rtype: None
    """
    return 'do some magic!'


def root_get():
    """
    def hello():
    

    :rtype: None
    """
    return 'do some magic!'


def solver_solver_id_get(solver_id):
    """
    def getSolver(solver_id):
    
    :param solver_id: solver_id
    :type solver_id: str

    :rtype: None
    """
    return 'do some magic!'


def summaries_collaborative_get():
    """
    def summariesHandlerCollab():
    

    :rtype: None
    """
    return 'do some magic!'


def summaries_workflowexecution_get():
    """
    def summariesHandlerWorkflow():
    

    :rtype: None
    """
    return 'do some magic!'


def was_derived_from_id_get(id):
    """
    def wasDerivedFrom(id):
    
    :param id: id
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def workflow_delete_runid_post(runid):
    """
    workflow_delete_runid_post
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'


def workflow_edit_runid_post(runid):
    """
    workflow_edit_runid_post
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'


def workflow_export_data_id_get(id):
    """
    def exportDataProvenance(id):
    
    :param id: id
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def workflow_export_runid_get(runid):
    """
    def exportRunProvenance(runid):
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'


def workflow_get():
    """
    def workflowsHandler():
    

    :rtype: None
    """
    return 'do some magic!'


def workflow_insert_post():
    """
    workflow_insert_post
    

    :rtype: None
    """
    return 'do some magic!'


def workflow_runid_delete(runid):
    """
    workflow_runid_delete
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'


def workflow_runid_get(runid):
    """
    def workflowInfoHandler(runid):
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'


def workflow_summaries_get():
    """
    def summariesHandler():
    

    :rtype: None
    """
    return 'do some magic!'


def workflow_user_user_get(user):
    """
    def getUserRuns(user):
    
    :param user: user
    :type user: str

    :rtype: None
    """
    return 'do some magic!'


def workflowexecution_run_id_export_get(run_id):
    """
    def _exportRunProvenance(run_id):
    
    :param run_id: run_id
    :type run_id: str

    :rtype: None
    """
    return 'do some magic!'


def workflowexecutions_get():
    """
    def getWorkflowExecutions():
    

    :rtype: None
    """
    return 'do some magic!'


def workflowexecutions_insert_post():
    """
    workflowexecutions_insert_post
    

    :rtype: None
    """
    return 'do some magic!'


def workflowexecutions_runid_delete(runid):
    """
    workflowexecutions_runid_delete
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'


def workflowexecutions_runid_delete_post(runid):
    """
    workflowexecutions_runid_delete_post
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'


def workflowexecutions_runid_edit_post(runid):
    """
    workflowexecutions_runid_edit_post
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'


def workflowexecutions_runid_get(runid):
    """
    def getWorkflowInfo(runid):
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'


def workflowexecutions_runid_instances_get(runid):
    """
    def getInstancesMonitoring(runid):
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'


def workflowexecutions_runid_showactivity_get(runid):
    """
    def getMonitoring(runid):
    
    :param runid: runid
    :type runid: str

    :rtype: None
    """
    return 'do some magic!'
