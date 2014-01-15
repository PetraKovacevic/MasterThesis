##############################################################################

from kivy.logger import Logger
from twisted.internet import protocol

##############################################################################

# Client Factory, which remembers the root widget you give it
class TCPClientFactoryWithRoot(protocol.ClientFactory):
    def __init__(self, app_root, client):
        self.app_root = app_root
        self.protocol = client
        self.protocol.app_root = app_root # Tell the protocol about the app_root widget

    def clientConnectionLost(self, conn, reason):
        Logger.debug("Network: connection in %s lost, %s %s" % (self.__class__, conn, reason))


    def clientConnectionFailed(self, conn, reason):
        Logger.debug("Network: connection in %s failed, %s %s" % (self.__class__, conn, reason))

##############################################################################

# Server Factory, which remembers the root widget you give it
class TCPServerFactoryWithRoot(protocol.Factory):
    protocol = None

    def __init__(self, app_root, client):
        self.app_root = app_root
        self.protocol = client
        self.protocol.app_root = app_root # Tell the protocol about the root widget

##############################################################################
