domain=edeposit.policy
#../../../../../bin/i18ndude rebuild-pot --pot $domain.pot --create $domain  ../
#../../../../../bin/i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po

../../../../../bin/i18ndude rebuild-pot --pot plone.pot --create plone ../profiles
../../../../../bin/i18ndude sync --pot plone.pot cs/LC_MESSAGES/plone.po
msgfmt -o cs/LC_MESSAGES/plone.mo cs/LC_MESSAGES/plone.po
