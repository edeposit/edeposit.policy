# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import uuid
from logging import getLogger
import itertools
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

sendEmailToISBNGeneration = sendEmailFactory("worklist-waiting-for-isbn-generation",
                                             ['stavel.jan@gmail.com','martin.zizala@nkp.cz'],
                                             "Dokumenty cekajici na prideleni ISBN")

sendEmailToISBNSubjectValidation = sendEmailFactory("worklist-waiting-for-isbn-subject-validation",
                                                    ['stavel.jan@gmail.com','martin.zizala@nkp.cz'],
                                                    "Dokumenty cekajici na vecnou kontrolu ISBN")

sendEmailWithOriginalFilesWaitingForAleph = sendEmailFactory("worklist-waiting-for-aleph",
                                                             ['stavel.jan@gmail.com','martin.zizala@nkp.cz'],
                                                             "Dokumenty cekajici na Aleph")

sendEmailToAcquisition = sendEmailFactory("worklist-waiting-for-acquisition",
                                          ['stavel.jan@gmail.com','martin.zizala@nkp.cz'],
                                          "Dokumenty cekajici na Akvizici")

sendEmailToDescriptiveCataloguingPreparing \
    = sendEmailFactory("worklist-waiting-for-descriptive-cataloguing-preparing",
                       ['stavel.jan@gmail.com','jaroslava.svobodova@nkp.cz'],
                       "Dokumenty cekajici na přípravu jmenné katalogizace")

sendEmailToDescriptiveCataloguingReviewPreparing \
    = sendEmailFactory("worklist-waiting-for-descriptive-cataloguing-review-preparing",
                       ['stavel.jan@gmail.com','jaroslava.svobodova@nkp.cz'],
                       "Dokumenty cekajici na přípravu jmenné revize")

sendEmailToSubjectCataloguingPreparing \
    = sendEmailFactory("worklist-waiting-for-subject-cataloguing-preparing",
                       ['stavel.jan@gmail.com','jaroslava.svobodova@nkp.cz'],
                       "Dokumenty cekajici na přípravu věcné katalogizace")

sendEmailToSubjectCataloguingReviewPreparing \
    = sendEmailFactory("worklist-waiting-for-subject-cataloguing-review-preparing",
                       ['stavel.jan@gmail.com','jaroslava.svobodova@nkp.cz'],
                       "Dokumenty cekajici na přípravu věcné revize")

def sendEmailToGroupFactory(groupname):
    def sendEmailToGroup(wfStateInfo):
        context = wfStateInfo.object
        for member in api.user.get_users(groupname=groupname):
            username = member.id
            email = member.getProperty('email')
            view_name = 'worklist-waiting-for-user'
            subject = u"Jmenna katalogizace pro: " + username
            request = context.REQUEST
            request['userid']=username
            view = api.content.get_view(name=view_name, context = context, request = request)
            api.portal.send_email(recipient=",".join(['stavel.jan@gmail.com',email,]), subject=subject, body=view())

    return sendEmailToGroup

sendEmailToGroupDescriptiveCataloguers = sendEmailToGroupFactory('Descriptive Cataloguers')
sendEmailToGroupDescriptiveCataloguingReviewers = sendEmailToGroupFactory('Descriptive Cataloguing Reviewers')
sendEmailToGroupSubjectCataloguers = sendEmailToGroupFactory('Subject Cataloguers')
sendEmailToGroupSubjectCataloguingReviewers = sendEmailToGroupFactory('Subject Cataloguing Reviewers')

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
        dict( name = "originalfiles-waiting-for-isbn-generation",
              title= u"Originály čekající na přidělení ISBN",
              query= queryForStates('ISBNGeneration'),
              group = 'ISBN Agency Members'
          ),
        dict( name = "originalfiles-waiting-for-aleph",
              title= u"Originály čekající na Aleph",
              query= queryForStates('waitingForAleph'),
              group = 'Acquisition Administrators',
          ),
        dict( name = "originalfiles-waiting-for-acquisition",
              title= u"Originály čekající na Akvizici",
              query= queryForStates('acquisition'),
              group = 'Acquisitors',
          ),
        dict( name = "originalfiles-waiting-for-isbn-subject-validation",
              title= u"Originály čekající na věcnou kontrolu ISBN",
              query= queryForStates('ISBNSubjectValidation'),
              group= 'ISBN Agency Members',
          ),
        dict( name = "originalfiles-waiting-for-descriptive-cataloguing-preparing",
              title= u"Originály čekající na přípravu jmenné katalogizace",
              query= queryForStates('descriptiveCataloguingPreparing'),
              group= 'Descriptive Cataloguing Administrators',
          ),
        dict( name = "originalfiles-waiting-for-descriptive-cataloguing-review-preparing",
              title= u"Originály čekající na přípravu jmenné revize",
              query= queryForStates('descriptiveCataloguingReviewPreparing'),
              group= 'Descriptive Cataloguing Administrators',
          ),
        dict( name = "originalfiles-waiting-for-subject-cataloguing-preparing",
              title= u"Originály čekající na přípravu věcné katalogizace",
              query= queryForStates('subjectCataloguingPreparing'),
              group= 'Subject Cataloguing Administrators',
          ),
        dict( name = "originalfiles-waiting-for-subject-cataloguing-review-preparing",
              title= u"Originály čekající na přípravu věcné revize",
              query= queryForStates('subjectCataloguingReviewPreparing'),
              group= 'Subject Cataloguing Administrators',
          ),
        dict( name = "originalfiles-waiting-for-renew-aleph-records",
              title= u"Originály čekající na akci v Alephu",
              query= queryForStates(
                'acquisition',
                'ISBNSubjectValidation',
                'subjectCataloguing',
                'subjectCataloguingReview',
                'descriptiveCataloguing',
                'descriptiveCataloguingReview',
                ),
              group= 'Subject Cataloguing Administrators',
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
            api.group.grant_roles(groupname=collection['group'],
                                  roles=['Reader',],
                                  obj=content)
            
    def createGroupUsersCollections(context, groupname, indexName, state, readerGroup):
        members = api.user.get_users(groupname=groupname)
        for username in map(lambda member: member.id, members):
            collectionName = 'originalfiles-waiting-for-user-' + username
            if collectionName not in context.keys():
                title = u"Originály čekající na: " + username
                query = queryForStates(state)
                queryForUser = [{ 'i': indexName,                     
                                  'o': 'plone.app.querystring.operation.string.is',
                                  'v': username }]
                collection = api.content.create( id=collectionName, 
                                                 container=context, 
                                                 type='Collection',
                                                 title=title, 
                                                 query = query + queryForUser)
                api.group.grant_roles(groupname="Descriptive Cataloguing Administrators",
                                      roles=['Reader',],  obj=collection)
                api.user.grant_roles(username=username, roles=['Reader',], obj=collection)
                
    createGroupUsersCollections(context=context, 
                                groupname="Descriptive Cataloguers",
                                indexName="getAssignedDescriptiveCataloguer",
                                state="descriptiveCataloguing",
                                readerGroup = "Descriptive Cataloguing Administrators",
                            )

    createGroupUsersCollections(context=context, 
                                groupname="Descriptive Cataloguing Reviewers",
                                indexName="getAssignedDescriptiveCataloguingReviewer",
                                state="descriptiveCataloguingReview",
                                readerGroup = "Descriptive Cataloguing Administrators",
                            )

    createGroupUsersCollections(context=context, 
                                groupname="Subject Cataloguers",
                                indexName="getAssignedSubjectCataloguer",
                                state="subjectCataloguing",
                                readerGroup = "Subject Cataloguing Administrators",
                            )

    createGroupUsersCollections(context=context, 
                                groupname="Subject Cataloguing Reviewers",
                                indexName="getAssignedSubjectCataloguingReviewer",
                                state="subjectCataloguingReview",
                                readerGroup = "Subject Cataloguing Administrators",
                            )


def loadSysNumbersFromAleph(wfStateInfo):
    producentsFolder = wfStateInfo.object
    collection = producentsFolder['originalfiles-waiting-for-aleph']
    originalFiles = map(lambda item: item.getObject(), collection.results(batch=False))
    wft = api.portal.get_tool('portal_workflow')
    for of in originalFiles:
        wft.doActionFor(of,'searchSysNumber')
    pass

def renewAlephRecords(wfStateInfo):
    producentsFolder = wfStateInfo.object
    collection = producentsFolder['originalfiles-waiting-for-renew-aleph-records']
    originalFiles = map(lambda item: item.getObject(), collection.results(batch=False))
    wft = api.portal.get_tool('portal_workflow')
    for of in originalFiles:
        wft.doActionFor(of,'renewAlephRecords')
    pass
