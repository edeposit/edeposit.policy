# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import uuid
from logging import getLogger
import itertools
from functools import reduce


logger = getLogger('edeposit.polici.wf_scripts')

def submitISBNChecks(wfStateInfo):
    logger.info("submitISBNChecks")
    print "submit isbn checks"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']
    isbns = filter(lambda item: item,
                   [epublication.isbn_souboru_publikaci] + \
                   [ii.isbn for ii in originalFiles.results()])

    with api.env.adopt_user(username="system"):
        for isbn in isbns:
            createContentInContainer(systemMessages, 'edeposit.content.isbnvalidationrequest',
                                     title = "Kontrola ISBN: " + isbn,
                                     isbn = isbn
                                 )
            
            createContentInContainer(systemMessages,  'edeposit.content.isbncountrequest',
                                     title = u"Zjištění duplicity ISBN: " + isbn,
                                     isbn = isbn
                                 )
            pass
        pass

def checkISBNsStatus(wfStateInfo):
    logger.info("checkISBNsStatus")
    print "check isbns status"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']
    wft = api.portal.get_tool('portal_workflow')
    isbns = filter(lambda item: item,
                   [epublication.isbn_souboru_publikaci] + \
                   [ii.isbn for ii in originalFiles.results()])


    def isbnISOK(result,item):
        k,v = item

        def findProperMessage(result, item):
            msg = item[1]
            if hasattr(msg,'is_valid'):
                result['is_valid'].add(msg.is_valid)
            if hasattr(msg,'num_of_records'): 
                result['num_of_records'].add(msg.num_of_records)
            return result

        properMessages = reduce( findProperMessage, v, {'is_valid':set(), 'num_of_records': set()} )
        # alespon jeden is_valid
        # vsechny is_valid musi byt OK

        # alespon jeden num_of_records
        # vsechny musi byt 0
        result[k] = properMessages
        return result

    with api.env.adopt_user(username="system"):
        # for each isbn must exists request and response in system
        # messages
        itemsByISBN = reduce( isbnISOK,
                              itertools.groupby(systemMessages.items(), key=lambda item: item[1].isbn),
                              dict() )

        # isbns = ['978-0-306-40615-7',]
        # itemsByISBN = {'978-0-306-40615-7': {'num_of_records': set([0]), 'is_valid': set([True])}}
        # statuses = itemsByISBN['978-0-306-40615-7']
        
        def isbnISOK(isbn):
            statuses = itemsByISBN.get(isbn,{'num_of_records':set(),'is_valid':set()})
            return statuses['is_valid'] == set([True]) and statuses['num_of_records'] == set([0])

        isbnStatuses = [ (isbn,isbnISOK(isbn)) for isbn in isbns]
        if set([ii[1] for ii in isbnStatuses]) == set([True]):
            # vsechny ISBN jsou zkontrolovane
            print "all isbns are valid"
            wft.doActionFor(epublication, 'allISBNsAreValid')
            print "all files are virus free"
            wft.doActionFor(epublication,'allFilesAreVirusFree')
            print "all files has thumbnail"
            wft.doActionFor(epublication,'allThumbnailsOK')
            pass

        # existuje nejake s chybou?
        pass
    pass


def submitAntivirusChecks(wfStateInfo):
    logger.info("submitAntivirusChecks")
    print "submit antivirus checks"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']

    with api.env.adopt_user(username="system"):
        for originalFile in originalFiles.results():
            # createContentInContainer(systemMessages, 'edeposit.content.isbnvalidationrequest',
            #                          title = "Kontrola ISBN: " + isbn,
            #                          isbn = isbn
            #                      )
            
            # createContentInContainer(systemMessages,  'edeposit.content.isbncountrequest',
            #                          title = u"Zjištění duplicity ISBN: " + isbn,
            #                          isbn = isbn
            #                      )
            pass
        pass

def submitExportToAleph(wfStateInfo):
    logger.info("submit export to Aleph")
    print "submit export to Aleph"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']

    with api.env.adopt_user(username="system"):
        for originalFile in originalFiles.results():
            createContentInContainer(systemMessages, 'edeposit.content.alephexportrequest',
                                     title = "Export do Alephu: " + originalFile.id,
                                     originalFileID = originalFile.id,
                                     isbn = originalFile.isbn,
                                 )
            pass
        pass
