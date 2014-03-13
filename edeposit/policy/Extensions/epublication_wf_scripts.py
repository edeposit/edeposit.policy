# -*- coding: utf-8 -*-
from plone import api
def submitISBNChecks(wfStateInfo):
    epublication = wfStateInfo.object
    epublication.objectItems()
    originalFiles = epublication['original-files']
    isbns = filter(lambda item: item,
                   [epublication.isbn_souboru_publikaci] + \
                   [ii.isbn for ii in originalFiles.results()])
    with api.env.adopt_user(username="system"):
        wft = api.portal.get_tool('portal_workflow')
        for isbn in isbns:
            wft.doActionFor(epublication,"notifyISBNwasSentForValidation", comment="ISBN: " + isbn)
        pass
    pass
