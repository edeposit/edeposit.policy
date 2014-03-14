# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import uuid

def sendISBNCheckToAMQP(isbn):
    return str(uuid.uuid1())

def sendISBNCountToAMQP(isbn):
    return str(uuid.uuid1())

def submitISBNChecks(wfStateInfo):
    epublication = wfStateInfo.object
    epublication.objectItems()
    originalFiles = epublication['original-files']
    isbns = filter(lambda item: item,
                   [epublication.isbn_souboru_publikaci] + \
                   [ii.isbn for ii in originalFiles.results()])
    with api.env.adopt_user(username="system"):
        wft = api.portal.get_tool('portal_workflow')
        systemMessages = epublication['system-messages']
        for isbn in isbns:
            uuid = sendISBNCheckToAMQP(isbn)
            wft.doActionFor(epublication,"notifyISBNwasSentForValidation",  
                            comment="ISBN: " + isbn)
            createContentInContainer(systemMessages,
                                     'edeposit.content.isbncheckrequest',
                                     title = "Kontrola ISBN: " + isbn,
                                     uuid = uuid,
                                     isbn = isbn
                                 )
            uuid = sendISBNCountToAMQP(isbn)
            wft.doActionFor(epublication,"notifyISBNwasSentForCount", 
                            comment="ISBN: " + isbn)
            createContentInContainer(systemMessages,
                                     'edeposit.content.isbncountrequest',
                                     title = u"Zjištění duplicity ISBN: " + isbn,
                                     uuid = sendISBNCountToAMQP(isbn),
                                     isbn = isbn
                                 )

        pass
    pass
