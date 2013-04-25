import unittest2 as unittest
from Products.CMFCore.utils import getToolByName

from edeposit.policy.testing import EDEPOSIT_POLICY_INTEGRATION_TESTING

class TestSetup(unittest.TestCase):
    
    layer = EDEPOSIT_POLICY_INTEGRATION_TESTING
    
    WORKFLOW_NAME = 'edeposit_manual_acquisition_workflow'

    def test_portal_title(self):
        portal = self.layer['portal']
        self.assertEqual("E-Deposit Site", portal.getProperty('title'))
    
    def test_portal_description(self):
        portal = self.layer['portal']
        self.assertEqual("Welcome to E-Deposit", portal.getProperty('description'))
    
    def test_role_added(self):
        portal = self.layer['portal']
        self.assertTrue("Publishers" in portal.validRoles())

    def test_workflow_installed(self):
        portal = self.layer['portal']
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertTrue(self.WORKFLOW_NAME in workflow)

    def test_workflows_mapped(self):
        portal = self.layer['portal']
        workflow = getToolByName(portal, 'portal_workflow')
        # self.assertEqual((self.WORKFLOW_NAME,), workflow.getDefaultChain())

    def test_view_permisison_for_publisher(self):
        portal = self.layer['portal']
        self.assertTrue('View' in [r['name']
                                   for r in portal.permissionsOfRole('Reviewer')
                                   if r['selected']])
        self.assertTrue('View' in [r['name']
                                   for r in portal.permissionsOfRole('Publisher')
                                   if r['selected']])

    def test_publishers_group_added(self):
        portal = self.layer['portal']
        acl_users = portal['acl_users']
        self.assertEqual(1, len(acl_users.searchGroups(name='Publishers')))

    def test_PloneFormGen_installed(self):
        portal = self.layer['portal']
        portal_types = getToolByName(portal, 'portal_types')
        self.assertTrue("FormFolder" in portal_types)
