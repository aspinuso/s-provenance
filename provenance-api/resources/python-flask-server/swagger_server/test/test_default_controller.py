# coding: utf-8

from __future__ import absolute_import

from . import BaseTestCase
from six import BytesIO
from flask import json


class TestDefaultController(BaseTestCase):
    """ DefaultController integration test stubs """

    def test_activities_run_id_get(self):
        """
        Test case for activities_run_id_get

        def activitiesHandler(runId):
        """
        response = self.client.open('//activities/{runId}'.format(runId='runId_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_components_compid_get(self):
        """
        Test case for components_compid_get

        def getComponentDetails(compid):
        """
        response = self.client.open('//components/{compid}'.format(compid='compid_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_data_data_id_export_get(self):
        """
        Test case for data_data_id_export_get

        def _exportDataProvenance(data_id):
        """
        response = self.client.open('//data/{data_id}/export'.format(data_id='data_id_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_data_get(self):
        """
        Test case for data_get

        def getData():
        """
        response = self.client.open('//data',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_data_granule_terms_get(self):
        """
        Test case for data_granule_terms_get

        def getDataGranuleTerms():
        """
        response = self.client.open('//dataGranuleTerms',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_derived_data_id_get(self):
        """
        Test case for derived_data_id_get

        def derivedData(id):
        """
        response = self.client.open('//derivedData/{id}'.format(id='id_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_entities_method_get(self):
        """
        Test case for entities_method_get

        def getEntitiesByMethod(method):
        """
        response = self.client.open('//entities/{method}'.format(method='method_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_entities_method_post(self):
        """
        Test case for entities_method_post

        
        """
        response = self.client.open('//entities/{method}'.format(method='method_example'),
                                    method='POST')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_instances_instid_get(self):
        """
        Test case for instances_instid_get

        def getInstanceDetails(instid): 
        """
        response = self.client.open('//instances/{instid}'.format(instid='instid_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_invocations_invocid_get(self):
        """
        Test case for invocations_invocid_get

        def getInvocationDetails(invocid):
        """
        response = self.client.open('//invocations/{invocid}'.format(invocid='invocid_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_root_get(self):
        """
        Test case for root_get

        def hello():
        """
        response = self.client.open('//',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_solver_solver_id_get(self):
        """
        Test case for solver_solver_id_get

        def getSolver(solver_id):
        """
        response = self.client.open('//solver/{solver_id}'.format(solver_id='solver_id_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_summaries_collaborative_get(self):
        """
        Test case for summaries_collaborative_get

        def summariesHandlerCollab():
        """
        response = self.client.open('//summaries/collaborative',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_summaries_workflowexecution_get(self):
        """
        Test case for summaries_workflowexecution_get

        def summariesHandlerWorkflow():
        """
        response = self.client.open('//summaries/workflowexecution',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_was_derived_from_id_get(self):
        """
        Test case for was_derived_from_id_get

        def wasDerivedFrom(id):
        """
        response = self.client.open('//wasDerivedFrom/{id}'.format(id='id_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflow_delete_runid_post(self):
        """
        Test case for workflow_delete_runid_post

        
        """
        response = self.client.open('//workflow/delete/{runid}'.format(runid='runid_example'),
                                    method='POST')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflow_edit_runid_post(self):
        """
        Test case for workflow_edit_runid_post

        
        """
        response = self.client.open('//workflow/edit/{runid}'.format(runid='runid_example'),
                                    method='POST')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflow_export_data_id_get(self):
        """
        Test case for workflow_export_data_id_get

        def exportDataProvenance(id):
        """
        response = self.client.open('//workflow/export/data/{id}'.format(id='id_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflow_export_runid_get(self):
        """
        Test case for workflow_export_runid_get

        def exportRunProvenance(runid):
        """
        response = self.client.open('//workflow/export/{runid}'.format(runid='runid_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflow_get(self):
        """
        Test case for workflow_get

        def workflowsHandler():
        """
        response = self.client.open('//workflow/',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflow_insert_post(self):
        """
        Test case for workflow_insert_post

        
        """
        response = self.client.open('//workflow/insert',
                                    method='POST')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflow_runid_delete(self):
        """
        Test case for workflow_runid_delete

        
        """
        response = self.client.open('//workflow/{runid}'.format(runid='runid_example'),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflow_runid_get(self):
        """
        Test case for workflow_runid_get

        def workflowInfoHandler(runid):
        """
        response = self.client.open('//workflow/{runid}'.format(runid='runid_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflow_summaries_get(self):
        """
        Test case for workflow_summaries_get

        def summariesHandler():
        """
        response = self.client.open('//workflow/summaries',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflow_user_user_get(self):
        """
        Test case for workflow_user_user_get

        def getUserRuns(user):
        """
        response = self.client.open('//workflow/user/{user}'.format(user='user_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflowexecution_run_id_export_get(self):
        """
        Test case for workflowexecution_run_id_export_get

        def _exportRunProvenance(run_id):
        """
        response = self.client.open('//workflowexecution/{run_id}/export'.format(run_id='run_id_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflowexecutions_get(self):
        """
        Test case for workflowexecutions_get

        def getWorkflowExecutions():
        """
        response = self.client.open('//workflowexecutions',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflowexecutions_insert_post(self):
        """
        Test case for workflowexecutions_insert_post

        
        """
        response = self.client.open('//workflowexecutions/insert',
                                    method='POST')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflowexecutions_runid_delete(self):
        """
        Test case for workflowexecutions_runid_delete

        
        """
        response = self.client.open('//workflowexecutions/{runid}'.format(runid='runid_example'),
                                    method='DELETE')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflowexecutions_runid_delete_post(self):
        """
        Test case for workflowexecutions_runid_delete_post

        
        """
        response = self.client.open('//workflowexecutions/{runid}/delete'.format(runid='runid_example'),
                                    method='POST')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflowexecutions_runid_edit_post(self):
        """
        Test case for workflowexecutions_runid_edit_post

        
        """
        response = self.client.open('//workflowexecutions/{runid}/edit'.format(runid='runid_example'),
                                    method='POST')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflowexecutions_runid_get(self):
        """
        Test case for workflowexecutions_runid_get

        def getWorkflowInfo(runid):
        """
        response = self.client.open('//workflowexecutions/{runid}'.format(runid='runid_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflowexecutions_runid_instances_get(self):
        """
        Test case for workflowexecutions_runid_instances_get

        def getInstancesMonitoring(runid):
        """
        response = self.client.open('//workflowexecutions/{runid}/instances'.format(runid='runid_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_workflowexecutions_runid_showactivity_get(self):
        """
        Test case for workflowexecutions_runid_showactivity_get

        def getMonitoring(runid):
        """
        response = self.client.open('//workflowexecutions/{runid}/showactivity'.format(runid='runid_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
