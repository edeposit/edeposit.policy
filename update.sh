domain=edeposit.policy
path=edeposit/policy
mkdir -p $path/locales/cs/LC_MESSAGES

touch $path/locales/cs/LC_MESSAGES/$domain.po
touch $path/locales/$domain.pot
../../bin/i18ndude rebuild-pot --pot $path/locales/$domain.pot --create $domain  $path
../../bin/i18ndude sync --pot $path/locales/$domain.pot $path/locales/cs/LC_MESSAGES/$domain.po
msgfmt -o $path/locales/cs/LC_MESSAGES/$domain.mo $path/locales/cs/LC_MESSAGES/$domain.po

touch $path/locales/cs/LC_MESSAGES/plone.po
touch $path/locales/plone.pot
../../bin/i18ndude rebuild-pot --pot $path/locales/plone.pot --create plone $path/profiles
../../bin/i18ndude sync --pot $path/locales/plone.pot $path/locales/cs/LC_MESSAGES/plone.po
msgfmt -o $path/locales/cs/LC_MESSAGES/plone.mo $path/locales/cs/LC_MESSAGES/plone.po
