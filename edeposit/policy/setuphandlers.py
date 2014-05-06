# -*- coding: utf-8 -*-
from edeposit.policy import MessageFactory as _
from Products.CMFCore.utils import getToolByName
from plone import api
from zope.interface import implements
from zope.component import adapts, queryUtility

from zope.container.interfaces import INameChooser

from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser

from plone.portlets.interfaces import IPortletManager
from plone.portlets.constants import USER_CATEGORY, GROUP_CATEGORY

from plone.app.portlets.interfaces import IDefaultDashboard
from plone.app.portlets import portlets

from plone.app.portlets.storage import UserPortletAssignmentMapping, GroupDashboardPortletAssignmentMapping

groups = (
    { 'group_id': 'Acquisitors',
      'title': 'E-Deposit: Acquisitors',
      'description': '',
      'roles': ['E-Deposit: Acquisitor',]
  },
    { 'group_id': 'Acquisition Administrators',
      'title': 'E-Deposit: Acquisitor Administrators',
      'description': 'Users that can assign work for acquisitors',
      'roles': []
  },
    { 'group_id': 'Librarians',
      'title': 'E-Deposit: Librarians',
      'description': '',
      'roles': []
  },
    { 'group_id': 'Library Administrators',
      'title': 'E-Deposit: Librarian Administrators',
      'description': '',
      'roles': ['E-Deposit: Librarian Administrator',]
  },
    { 'group_id': 'Producent Administrators',
      'title': 'E-Deposit: Producent Administrators',
      'description': 'Producent administrators can assign new administrators and editors for given producent',
      'roles': []
  },
    { 'group_id': 'Producent Contributors',
      'title': 'E-Deposit: Producent Contributors',
      'description': '',
      'roles': []
  },
    { 'group_id': 'Producent Editors',
      'title': 'E-Deposit: Producent Editors',
      'description': '',
      'roles': []
  },
    { 'group_id': 'RIV Reviewers',
      'title': 'E-Deposit: RIV Reviewers',
      'description': '',
      'roles': []
  },
    { 'group_id': 'Testers',
      'title': 'E-Deposit: Testers',
      'description': '',
      'roles': ['E-Deposit: Producent Administrator',
                'E-Deposit: Producent Editor',
                'E-Deposit: Producent Contributor']
  },
)

def setupGroups(portal):
    gtool = getToolByName(portal, 'portal_groups')
    acl_users = getToolByName(portal, 'acl_users')
    group_ids = acl_users.source_groups.getGroupIds()
    for group in groups:
        if not group['group_id'] in group_ids:
            gtool.addGroup(group['group_id'], roles=group['roles'])
            gtool.editGroup(group['group_id'], title = group['title'], description=group['description'])

def createAgreementFile(portal):
    setup_tool = portal.portal_setup
    profiles = setup_tool.listProfileInfo()
    [ (pp['title'],pp['id']) for pp in  profiles]
    [ pp['id'] for pp in  profiles]
    linkName='smlouva-o-poskytovani-sluzeb'
    if linkName not in portal.objectIds():
        portal.invokeFactory('edeposit.user.agreementfile',  linkName,  title=u"Smlouva s Národní knihovnou")
    pass

def createUsers(portal):
    if api.user.get(username="system"):
        return
    properties = dict(
        fullname='E-Deposit system user',
        location='Prague',
    )
    api.user.create(username="system",
                    email="edeposit@email.cz",
                    password="shoj98Phai9",
                )
    api.group.add_user(groupname='Administrators', username='system')
    api.group.add_user(groupname='Site Administrators', username='system')
    pass

def updateGroupDashboards(portal):
    groupid = 'Acquisitors'
    name = 'plone.dashboard1'
    column = queryUtility(IPortletManager,name)
    category = column.get('group',None)
    manager = category.get(groupid,None)
    #import sys,pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    if manager is None:
        manager =  GroupDashboardPortletAssignmentMapping(manager=name,  category=GROUP_CATEGORY, name=groupid)
        chooser = INameChooser(manager)
        # for assignment in assignments:
        #     manager[chooser.chooseName(None, assignment)] = assignment
    pass
    
def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('edeposit.policy.marker.txt') is None:
        return

    portal = context.getSite()
    setupGroups(portal)
    createUsers(portal)
    #updateGroupDashboards(portal)
    #createAgreementFile(portal)
