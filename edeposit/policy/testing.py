from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from zope.configuration import xmlconfig

class EDepositPolicy(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import edeposit.policy
        xmlconfig.file('configure.zcml', edeposit.policy, context=configurationContext)

        # # Install products that use an old-style initialize() function
        # z2.installProduct(app, 'Products.PythonField')
        # z2.installProduct(app, 'Products.TALESField')
        # z2.installProduct(app, 'Products.TemplateFields')
        # z2.installProduct(app, 'Products.PloneFormGen')
        pass


    def tearDownZope(self, app):
        # Uninstall products installed above
        # z2.uninstallProduct(app, 'Products.PloneFormGen')
        # z2.uninstallProduct(app, 'Products.TemplateFields')
        # z2.uninstallProduct(app, 'Products.TALESField')
        # z2.uninstallProduct(app, 'Products.PythonField')
        pass

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edeposit.policy:default')

EDEPOSIT_POLICY_FIXTURE = EDepositPolicy()
EDEPOSIT_POLICY_INTEGRATION_TESTING = IntegrationTesting( bases=(EDEPOSIT_POLICY_FIXTURE,), 
                                                          name="EDeposit:Integration")
