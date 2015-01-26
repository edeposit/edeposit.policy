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

from edeposit.content.amqp import IAMQPSender, IAMQPHandler
from collective.documentviewer.async import queueJob

import json
from five import grok

logger = getLogger('edeposit.originalfile.wf_scripts')

# (occur-1 "def " nil (list (current-buffer)) "*Occur: originalfile_wf_scripts.py/def*")
# (occur-1 "class " nil (list (current-buffer)) "*Occur: originalfile_wf_scripts.py/class*")

def submitDocumentViewer(wfStateInfo):
    originalfile = wfStateInfo.object
    if originalfile.getLayout() != 'documentviewer':
        originalfile.setLayout('documentviewer')

    queueJob(originalfile)

def submitAntivirusCheck(wfStateInfo):
    logger.info("submitAntivirusChecks")
    with api.env.adopt_user(username="system"):
        originalfile = wfStateInfo.object
        epublication = aq_parent(aq_inner(originalfile))
        getAdapter(originalfile,IAMQPSender,name="antivirus-check").send()
        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor(epublication, 
                        'notifySystemAction', 
                        comment=u"Antivirová kontrola pro: " + originalfile.file.filename)
        pass

def submitISBNValidation(wfStateInfo):
    print "submitISBNValidation"
    originalfile = wfStateInfo.object
    epublication = aq_parent(aq_inner(originalfile))
    with api.env.adopt_user(username="system"):
        getAdapter(originalfile,IAMQPSender,name="isbn-validate").send()
        comment=u"Automatická kontrola ISBN:%s, %s " % (originalfile.isbn, originalfile.file.filename)
        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor(epublication, 'notifySystemAction', comment=comment)

def submitISBNDuplicityCheck(wfStateInfo):
    print "submitISBN Duplicity Check"
    originalfile = wfStateInfo.object
    epublication = aq_parent(aq_inner(originalfile))
    with api.env.adopt_user(username="system"):
        getAdapter(originalfile, IAMQPSender, name="isbn-duplicity-check").send()
        comment=u"Automatická kontrola duplicity ISBN:%s, %s " % (originalfile.isbn, originalfile.file.filename)
        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor(epublication, 'notifySystemAction', comment=comment)

def submitExportToAleph(wfStateInfo):
    print "submit export to Aleph"
    originalfile = wfStateInfo.object
    epublication = aq_parent(aq_inner(originalfile))
    with api.env.adopt_user(username="system"):
        getAdapter(originalfile, IAMQPSender, name="export-to-aleph").send()
        comment=u"Export do Alephu ISBN:%s" % (originalfile.isbn, )
        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor(epublication, 'notifySystemAction', comment=comment)

def submitSysNumbersSearch(wfStateInfo):
    logger.info("submitSysNumberSearch")
    print "submit sysnumber search"
    originalfile = wfStateInfo.object
    epublication = aq_parent(aq_inner(originalfile))
    with api.env.adopt_user(username="system"):
        getAdapter(originalfile, IAMQPSender, name="sysnumber-aleph-search").send()
        comment=u"Dohledat sysNumber v Alephu ISBN:%s" % (originalfile.isbn, )
        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor(epublication, 'notifySystemAction', comment=comment)

def renewAlephRecords(wfStateInfo):
    logger.info("renewAlephRecords")
    print "renew Aleph Records"
    originalfile = wfStateInfo.object
    epublication = aq_parent(aq_inner(originalfile))
    with api.env.adopt_user(username="system"):
        getAdapter(originalfile, IAMQPSender, name="renew-aleph-records").send()
        comment=u"Synchronizace s Alephem, isbn:%s" % (originalfile.isbn, )
        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor(epublication, 'notifySystemAction', comment=comment)


def submitThumbnailGenerating(wfStateInfo):
    logger.info("submitThumbnailGenerating")
    print "submit thumbnail generating"
    originalfile = wfStateInfo.object
    epublication = aq_parent(aq_inner(originalfile))
    with api.env.adopt_user(username="system"):
        getAdapter(originalfile, IAMQPSender, name="generate-thumbnail").send()
        comment=u"Generovat náhled pro soubor:%s" % (originalfile.file.filename, )
        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor(epublication, 'notifySystemAction', comment=comment)

def submitVoucherGeneration(wfStateInfo):
    originalfile = wfStateInfo.object
    getAdapter(originalfile,IAMQPSender,name="voucher-generate").send()
    
def updateRelatedItems(wfStateInfo):
    logger.info("updateRelatedItems")
    print "update related items for original file"
    originalfile = wfStateInfo.object
    epublication = aq_parent(aq_inner(originalfile))
    intids = getUtility(IIntIds)
    originalfile.relatedItems = [RelationValue(intids.getId(epublication))]

def checkISBNsStatus(wfStateInfo):
    logger.info("checkISBNsStatus")
    print "check isbns status"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']
    wft = api.portal.get_tool('portal_workflow')

    def statusesForISBN(result,item):
        isbn,messages = item

        def findProperMessage(result, item):
            msg = item[1]
            if hasattr(msg,'is_valid'):
                result['is_valid'].add(msg.is_valid)
            if hasattr(msg,'num_of_records'): 
                result['num_of_records'].add(msg.num_of_records)
            return result

        statuses = reduce( findProperMessage, messages, {'is_valid':set(), 'num_of_records': set()} )
        result[isbn] = statuses
        return result
        
    statusesByISBN = reduce( statusesForISBN,
                          itertools.groupby(systemMessages.items(), key=lambda item: item[1].isbn),
                          dict() )
    
    with api.env.adopt_user(username="system"):
        # for each isbn must exists request and response in system
        # messages
        # isbns = ['978-0-306-40615-7',]
        # itemsByISBN = {'978-0-306-40615-7': {'num_of_records': set([0]), 'is_valid': set([True])}}
        # statuses = itemsByISBN['978-0-306-40615-7']
        
        def isbnStatus(itemsByISBN,isbn):
            statuses = itemsByISBN.get(isbn,{'num_of_records':set(),'is_valid':set()})
            return { 'is_valid': statuses['is_valid'],
                     'num_of_records': statuses['num_of_records'] }

        def statusISOK(status):
            return (status['is_valid'] == set([True]) and status['num_of_records'] == set([0]))
        
        isbnsWithError = filter(lambda isbn: not statusISOK(isbnStatus(statusesByISBN,isbn)), isbns)
        #if set([ii[1] for ii in isbnStatuses]) == set([True]):
        if not isbnsWithError:
            # vsechny ISBN jsou zkontrolovane
            print "all isbns are valid"
            wft.doActionFor(epublication, 'allISBNsAreValid')
            print "all files are virus free"
            wft.doActionFor(epublication,'allFilesAreVirusFree')
            print "all files has thumbnail"
            wft.doActionFor(epublication,'allThumbnailsOK')
            pass
        else:
            for (isbn,status) in map( lambda isbn: (isbn, isbnStatus(statusesByISBN,isbn)), isbnsWithError):
                if (status['num_of_records'] != set([]) and status['num_of_records'] != set([0])):
                    # duplicitni isbn
                    print "isbn je duplicitni: " + isbn
                if status['is_valid'] != set([]) and status['is_valid'] != set([True]):
                    # nevalidni zaznam
                    print "isbn neni validni: " + isbn
        pass
    pass

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


