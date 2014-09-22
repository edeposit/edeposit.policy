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

sendEmailToAcquisition = sendEmailFactory("worklist-for-acquisition",
                                          ['stavel.jan@gmail.com','martin.zizala@nkp.cz'],
                                          "Dokumenty cekajici na Akvizici")

sendEmailToCatalogization = sendEmailFactory("worklist-for-catalogization",
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
              title= u"Dokumenty čekající na přidělení ISBN",
              query= queryForStates('ISBNGeneration'),
              roles = ['E-Deposit: Producent Administrator','E-Deposit: Acquisitor','E-Deposit: ISBN Agency'],
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
            #api.group.grant_roles(groupname="Producents", roles=['Reader'], obj=content)
            #api.group.grant_roles(groupname="Producents", roles=['Reader'], obj=content)
    pass
