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
import isbn_validator
from edeposit.content.amqp import IAMQPSender, IAMQPHandler
from collective.documentviewer.async import queueJob

import json
from five import grok
from edeposit.content.tasks import IPloneTaskSender, DoActionFor

logger = getLogger('edeposit.eperiodical.wf_scripts')

# (occur-1 "def " nil (list (current-buffer)) "*Occur: originalfile_wf_scripts.py/def*")
# (occur-1 "class " nil (list (current-buffer)) "*Occur: originalfile_wf_scripts.py/class*")


def submitAMQPTaskUpdateLinksAtAleph(wfStateInfo):
    print "submit amqp task update links at Aleph"
    context = wfStateInfo.object
    with api.env.adopt_user(username="system"):
        IPloneTaskSender(DoActionFor(transition='submitUpdateLinksAtAleph', uid=context.UID())).send()

def submitUpdateLinksAtAleph(wfStateInfo):
    print "submit update links at Aleph"
    originalfile = wfStateInfo.object
    with api.env.adopt_user(username="system"):
        getAdapter(originalfile, IAMQPSender, name="update-links-at-aleph").send()

def submitSysNumbersSearch(wfStateInfo):
    logger.info("submitSysNumberSearch")
    print "submit sysnumber search"
    with api.env.adopt_user(username="system"):
        getAdapter(wfStateInfo.object, IAMQPSender, name="sysnumber-aleph-search").send()
        
def recordHasBeenChanged(wfStateInfo):
    logger.info("record has been changed")
    print "record has been changed"
    originalfile = wfStateInfo.object
    with api.env.adopt_user(username="system"):
        getAdapter(originalfile, IEmailSender, name="originalfile-has-been-changed").send()
        
def renewAlephRecords(wfStateInfo):
    logger.info("renewAlephRecords")
    print "renew Aleph Records"
    context = wfStateInfo.object
    with api.env.adopt_user(username="system"):
        getAdapter(context, IAMQPSender, name="load-aleph-records-by-title").send()
        getAdapter(context, IAMQPSender, name="renew-aleph-records-by-icz-sysnumber").send()

def loadAlephRecordsByTitle(wfStateInfo):
    logger.info("loadAlephRecords by title")
    with api.env.adopt_user(username="system"):
        getAdapter(wfStateInfo.object, IAMQPSender, name="load-aleph-records-by-title").send()

def renewAlephRecordsBySysNumber(wfStateInfo):
    logger.info("renewAlephRecords by SysNumber")
    with api.env.adopt_user(username="system"):
        getAdapter(wfStateInfo.object, IAMQPSender, name="renew-aleph-records-by-sysnumber").send()

def acquisitionOK(wfStateInfo):
    logger.info("acquisition passed OK")

def submitVoucherGeneration(wfStateInfo):
    originalfile = wfStateInfo.object
    getAdapter(originalfile,IAMQPSender,name="voucher-generate").send()

def checkExportStatuses(wfStateInfo):
    logger.info("checkExportStatuses")
    print "check export statuses"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']
    wft = api.portal.get_tool('portal_workflow')
    catalog = api.portal.get_tool('portal_catalog')
    folder_path = '/'.join(systemMessages.getPhysicalPath())
    exportResults = map(lambda brain: brain.getObject(), 
                        catalog(path={'query': folder_path, 'depth': 1},
                                portal_type = 'edeposit.content.alephexportresult')
                    )
    isbns = set(filter(lambda item: item, map(lambda ii: ii.isbn, originalFiles.results())))
    isbnsInExportResults = set(filter(lambda item: item, map(lambda result: result.isbn, exportResults)))
    with api.env.adopt_user(username="system"):
        # for each isbn must exists request and response in system messages
        if isbns == isbnsInExportResults:
            # vsechna ISBN jsou vyexportovana
            print "all isbns are exported"
            wft.doActionFor(epublication, 'allExportsToAlephOK')
            pass
        pass
    pass

def submitAMQPTaskClassificateError(wfStateInfo):
    print "submit amqp task to classificate amqp error"
    context = wfStateInfo.object
    with api.env.adopt_user(username="system"):
        IPloneTaskSender(DoActionFor(transition='classificateError', uid=context.UID())).send()


def classificateError(wfStateInfo):
    context = wfStateInfo.object
    classifiers = context.portal_catalog(portal_type="edeposit.amqp_errors.amqperrorclassificationfolder")
    classificatorFolder = classifiers and classifiers[0].getObject()
    #(status, prob) = classificatorFolder.classifyError('only Czech ISBN is required')
    pass

def alephLinkUpdateResponseOK(wfStateInfo):
    pass

def alephLinkUpdateResponseError(wfStateInfo):
    pass
