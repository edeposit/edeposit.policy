from edeposit.policy import MessageFactory as _
from Products.CMFCore.utils import getToolByName

groups = (
    { 'group_id': 'Acquisitors',
      'title': 'E-Deposit: Acquisitors',
      'description': '',
      'roles':['E-Deposit: Acquisitor',]
      },
    { 'group_id': 'Librarians',
      'title': 'E-Deposit: Librarians',
      'description': '',
      'roles': ['E-Deposit: Librarian',]
      },
    { 'group_id': 'Producents',
      'title': 'E-Deposit: Producents',
      'description': '',
      'roles': ['E-Deposit: Producent',]
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

def importVarious(context):
    """Miscellanous steps import handle
    """
    portal = context.getSite()
    setupGroups(portal)
