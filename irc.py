from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
import sys

class ChatBridge(irc.IRCClient):

    nickname = "skeetersbot"
    debug = False
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def joined(self, channel):
        pass

    def signedOn(self):
        self.join(self.factory.channel)

    def privmsg(self, user, channel, mesg):
        print(user.split("!")[0]+": "+mesg)

    def action(self, user, channel, mesg):
        pass

    def irc_NICK(self, prefix, params):
        pass

    def userlist(self):
        self.sendLine('NAMES %s' % self.factory.channel)
    
    def irc_RPL_NAMREPLY(self, *nargs):
        print( nargs[1][3:] )
    def irc_RPL_ENDOFNAMES(self, *nargs):
        print("NAMES COMPLETE")

    def irc_unknown(self, prefix, command, params):
        "Print all unhandled replies, for debugging."
        if self.debug :
            print ('UNKNOWN:', prefix, command, params)


class ChatBridgeFactory(protocol.ClientFactory):
    
    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = ChatBridge()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print( "connection failed:", reason)
        reactor.stop()


if __name__ == "__main__":
    f = ChatBridgeFactory(sys.argv[3])
    reactor.connectTCP(sys.argv[1], int(sys.argv[2]), f)

    reactor.run()
