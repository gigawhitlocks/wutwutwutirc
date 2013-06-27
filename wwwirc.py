from twisted.words.protocols import irc

from twisted.internet import reactor, protocol


class ChatBridge(irc.IRCClient):

    nickname = "skeetersbot"
    debug = False
    websocket = None

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.factory.websocket.connectToIRC()
        self.factory.websocket.write_message({"type":"chat",\
                "user":"NOTICE",\
                "message":"YOU HAVE JOINED "+self.factory.channel})

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def joined(self, channel):
        pass

    def signedOn(self):
        self.join(self.factory.channel)

    def privmsg(self, user, channel, mesg):
        if self.factory.websocket :
            self.factory.websocket.write_message({"type":"chat",\
                    "user":user.split("!")[0],
                    "message":mesg})
        else :
            print ("websocket not open")

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

    bridge = None
    
    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = ChatBridge()
        p.factory = self
        self.bridge = p

        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print( "connection failed:", reason)
        reactor.stop()

