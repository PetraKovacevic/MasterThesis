# connect and then disconnect
from kivy.logger import Logger
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import NetstringReceiver


class TCPSender(NetstringReceiver):
    def sendMessage(self, msg):
        self.sendString(msg)
        self.transport.loseConnection()

def sendMessage(p, msg):
    p.sendMessage(msg)

def printError(failure):
    Logger.debug("TCP Message Sender: {0}".format(failure))

