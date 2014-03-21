# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import uuid

def submitISBNChecks(wfStateInfo):
    epublication = wfStateInfo.object
    originalFiles = epublication['original-files']
    isbns = filter(lambda item: item,
                   [epublication.isbn_souboru_publikaci] + \
                   [ii.isbn for ii in originalFiles.results()])
    with api.env.adopt_user(username="system"):
        systemMessages = epublication['system-messages']
        for isbn in isbns:
            createContentInContainer(systemMessages, 'edeposit.content.isbncheckrequest',
                                     title = "Kontrola ISBN: " + isbn,
                                     uuid = str(uuid.uuid4()),
                                     isbn = isbn
                                 )
            
            createContentInContainer(systemMessages,  'edeposit.content.isbncountrequest',
                                     title = u"Zjištění duplicity ISBN: " + isbn,
                                     uuid = str(uuid.uuid4()),
                                     isbn = isbn
                                 )
        pass
    pass
