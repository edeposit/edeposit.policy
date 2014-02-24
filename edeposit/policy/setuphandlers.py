# -*- coding: utf-8 -*-
from edeposit.policy import MessageFactory as _
from Products.CMFCore.utils import getToolByName

groups = (   
    { 'group_id': 'Acquisitors',
      'title': 'E-Deposit: Acquisitors',
      'description': '',
      'roles': []
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
      'roles': []
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
    #import sys,pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    setup_tool = portal.portal_setup
    profiles = setup_tool.listProfileInfo()
    [ (pp['title'],pp['id']) for pp in  profiles]
    [ pp['id'] for pp in  profiles]
    linkName='smlouva-o-poskytovani-sluzeb'
    if linkName not in portal.objectIds():
        portal.invokeFactory('edeposit.user.agreementfile',  linkName,  title=u"Smlouva s Národní knihovnou")
    pass

def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('edeposit.policy.marker.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()
    setupGroups(portal)
    #createAgreementFile(portal)
