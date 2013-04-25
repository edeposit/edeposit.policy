from Products.CMFCore.utils import getToolByName

def setupGroups(portal):
    acl_users = getToolByName(portal, 'acl_users')
    if not acl_users.searchGroups(name='Publishers'):
        gtool = getToolByName(portal, 'portal_groups')
        gtool.addGroup('Publishers', roles=['Publisher'])

def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('edeposit.policy-various.txt') is None:
        return
    portal = context.getSite()
    setupGroups(portal)
