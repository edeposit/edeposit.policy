# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import uuid
from logging import getLogger
import itertools
from functools import reduce
from zope.app.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from Acquisition import aq_inner, aq_parent
from zope.component import queryUtility, getUtility, getAdapter
import base64
from edeposit.policy import MessageFactory as _

from edeposit.content.amqp import IAMQPSender, IAMQPHandler

import json
from five import grok

logger = getLogger('edeposit.producentfolder_wf_scripts')

# (occur-1 "def " nil (list (current-buffer)) "*Occur: originalfile_wf_scripts.py/def*")
# (occur-1 "class " nil (list (current-buffer)) "*Occur: originalfile_wf_scripts.py/class*")

def sendEmailFactory(view_name, recipients, subject):
    def handler(wfStateInfo):
        context = wfStateInfo.object
        view = api.content.get_view(name=view_name, context = context, request = context.REQUEST)
        api.portal.send_email(recipient=",".join(recipients), subject=subject, body=view())
    return handler

sendEmailToISBNAgency = sendEmailFactory("worklist-for-isbn-agency",
                                         ['stavel.jan@gmail.com','martin.zizala@nkp.cz'],
                                         "Dokumenty cekajici na prideleni ISBN")

sendEmailWithOriginalFilesWaitingForAleph = sendEmailFactory("worklist-waiting-for-aleph",
                                                             ['stavel.jan@gmail.com','martin.zizala@nkp.cz'],
                                                             "Dokumenty cekajici na Aleph")

sendEmailToAcquisition = sendEmailFactory("worklist-for-acquisition",
                                          ['stavel.jan@gmail.com','martin.zizala@nkp.cz'],
                                          "Dokumenty cekajici na Akvizici")

sendEmailToCataloguing = sendEmailFactory("worklist-for-cataloguing",
                                          ['stavel.jan@gmail.com','martin.zizala@nkp.cz'],
                                          "Dokumenty cekajici na jmennou katalogizaci")


def recreateCollections(wfStateInfo):
    context = wfStateInfo.object
    def queryForStates(*args):
        return [ {'i': 'portal_type',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['edeposit.content.originalfile']},
                 {'i': 'review_state',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': args},
                 {'i': 'path', 
                  'o': 'plone.app.querystring.operation.string.relativePath', 
                  'v': '../'}
                 ]

    collections = [ 
        dict( name = "originalfiles-for-isbn-agency",
              title= u"Originály čekající na přidělení ISBN",
              query= queryForStates('ISBNGeneration'),
              roles = ['E-Deposit: ISBN Agency Member'],
          ),
        dict( name = "originalfiles-waiting-for-aleph",
              title= u"Originály čekající na Aleph",
              query= queryForStates('waitingForAleph'),
              roles = ['E-Deposit: Acquisition Administrator'],
          ),
        dict( name = "originalfiles-waiting-for-acquisition",
              title= u"Originály čekající na Akvizici",
              query= queryForStates('acquisition'),
              roles = ['E-Deposit: Acquisitor'],
          ),
        dict( name = "originalfiles-waiting-for-descriptive-cataloguing-preparing",
              title= u"Originály čekající na přípravu jmenné katalogizace",
              query= queryForStates('descriptiveCataloguingPreparing'),
              roles = ['E-Deposit: Descriptive Cataloguing Administrator'],
          ),
        dict( name = "originalfiles-waiting-for-descriptive-cataloguing",
              title= u"Originály čekající na jmennou katalogizaci",
              query= queryForStates('descriptiveCataloguing'),
              roles = ['E-Deposit: Descriptive Cataloguer'],
          ),
        dict( name = "originalfiles-waiting-for-descriptive-cataloguing-review",
              title= u"Originály čekající na revizi jmenné katalogizace",
              query= queryForStates('descriptiveCataloguingReview'),
              roles = ['E-Deposit: Descriptive Cataloguing Reviewer'],
          ),
        dict( name = "originalfiles-waiting-for-subject-cataloguing-preparing",
              title= u"Originály čekající na přípravu věcné katalogizace",
              query= queryForStates('subjectCataloguingPreparing'),
              roles = ['E-Deposit: Subject Cataloguing Administrator'],
          ),
        dict( name = "originalfiles-waiting-for-subject-cataloguing",
              title= u"Originály čekající na věcnou katalogizaci",
              query= queryForStates('subjectCataloguing'),
              roles = ['E-Deposit: Subject Cataloguer'],
          ),
        dict( name = "originalfiles-waiting-for-subject-cataloguing-review",
              title= u"Originály čekající na revizi věcné katalogizace",
              query= queryForStates('subjectCataloguingReview'),
              roles = ['E-Deposit: Subject Cataloguing Reviewer'],
          ),
    ]

    for collection in collections:
        name = collection['name']
        if name not in context.keys():
            content = api.content.create (
                id=name,
                container=context,
                type='Collection', 
                title=collection['title'],
                query=collection['query']
            )
            api.group.grant_roles(groupname="ISBN Agency Members",
                                  roles=collection['roles'], obj=content)
    pass



def loadSysNumbersFromAleph(wfStateInfo):
    producentsFolder = wfStateInfo.object
    collection = producentsFolder['originalfiles-waiting-for-aleph']
    originalFiles = map(lambda item: item.getObject(), collection.results(batch=False))
    wft = api.portal.get_tool('portal_workflow')
    for of in originalFiles:
        wft.doActionFor(of,'searchSysNumber')
    pass
