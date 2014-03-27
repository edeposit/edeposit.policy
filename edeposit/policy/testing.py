from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.testing import z2
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

from zope.interface import Interface
from zope.component import getSiteManager
from collective.zamqp.interfaces import (
    IBrokerConnection,
    IProducer,
    IConsumer,
    IMessageArrivedEvent
)
from collective.zamqp.connection import BrokerConnection
from collective.zamqp.server import ConsumingServer
from collective.zamqp.producer import Producer
from collective.zamqp.consumer import Consumer

from zope.configuration import xmlconfig

class EDepositPolicy(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    trace_on = False
    zserver = True
    user_id="admin"
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import edeposit.policy
        import edeposit.user
        import edeposit.content
        xmlconfig.file('configure.zcml', edeposit.content, context=configurationContext) 
        xmlconfig.file('configure.zcml', edeposit.user, context=configurationContext)
        xmlconfig.file('configure.zcml', edeposit.policy, context=configurationContext)

        # # Install products that use an old-style initialize() function
        # z2.installProduct(app, 'Products.PythonField')
        # z2.installProduct(app, 'Products.TALESField')
        # z2.installProduct(app, 'Products.TemplateFields')
        # z2.installProduct(app, 'Products.PloneFormGen')

        # Define dummy request handler to replace ZPublisher

        def handler(app, request, response):
            from zope.event import notify
            from zope.component import createObject
            message = request.environ.get('AMQP_MESSAGE')
            event = createObject('AMQPMessageArrivedEvent', message)
            notify(event)

        # Define ZPublisher-based request handler to be used with zserver

        def zserver_handler(app, request, response):
            from ZPublisher import publish_module
            publish_module(app, request=request, response=response)

        # Create connections and consuming servers for registered
        # producers and consumers
        sm = getSiteManager()

        connections = []
        consuming_servers = []

        for producer in sm.getAllUtilitiesRegisteredFor(IProducer):
            if not producer.connection_id in connections:
                connection = BrokerConnection(producer.connection_id,
                                              virtual_host="aleph",
                )
                sm.registerUtility(connection, provided=IBrokerConnection,
                                   name=connection.connection_id)
                connections.append(connection.connection_id)

        for consumer in sm.getAllUtilitiesRegisteredFor(IConsumer):
            if not consumer.connection_id in connections:
                connection = BrokerConnection(consumer.connection_id,
                                              virtual_host="aleph"
                )
                sm.registerUtility(connection, provided=IBrokerConnection,
                                   name=connection.connection_id)
                connections.append(connection.connection_id)

            if not consumer.connection_id in consuming_servers:
                if self.zserver:
                    ConsumingServer(consumer.connection_id, 'plone',
                                    user_id=self.user_id,
                                    handler=zserver_handler,
                                    hostname='nohost',  # taken from z2.Startup
                                    port=80,
                                    use_vhm=False)
                else:
                    ConsumingServer(consumer.connection_id, 'plone',
                                    user_id=self.user_id,
                                    handler=handler,
                                    use_vhm=False)
                consuming_servers.append(consumer.connection_id)

        # Connect all connections

        from collective.zamqp import connection
        connection.connect_all()



    def tearDownZope(self, app):
        # Uninstall products installed above
        # z2.uninstallProduct(app, 'Products.PloneFormGen')
        # z2.uninstallProduct(app, 'Products.TemplateFields')
        # z2.uninstallProduct(app, 'Products.TALESField')
        # z2.uninstallProduct(app, 'Products.PythonField')
        pass

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edeposit.content:default')
        applyProfile(portal, 'edeposit.user:default')
        applyProfile(portal, 'edeposit.policy:default')


EDEPOSIT_POLICY_FIXTURE = EDepositPolicy()
EDEPOSIT_POLICY_ROBOT_TESTING = FunctionalTesting(
    bases=(EDEPOSIT_POLICY_FIXTURE,
           AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="E-Deposit Policy:Robot")

EDEPOSIT_POLICY_INTEGRATION_TESTING = IntegrationTesting( bases=(EDEPOSIT_POLICY_FIXTURE,), 
                                                          name="EDeposit:Integration")
