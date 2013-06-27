from tornado import websocket
import tornado.web
from tornado.options import define, options
#import tornado.auth
import tornado.autoreload
#import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


import tornado.platform.twisted
#from twisted.words.protocols import irc
tornado.platform.twisted.install()
from wwwirc import ChatBridgeFactory 
from twisted.internet import reactor

define("port", default=8000, help="run on the given port", type=int) 
class Application(tornado.web.Application):

    def __init__(self):
        settings = {}
        handlers = [(r"/ircbridge", ChatSocket),
                    (r"/js/(.*)", tornado.web.StaticFileHandler, {'path':'.'}),
                    (r"/", ViewHandler)
                    ]

        tornado.web.Application.__init__(self, handlers, **settings)

class ViewHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("view.html")

class ChatSocket(websocket.WebSocketHandler):

    def connectToIRC(self):
        self.irc_conn = self.factory.bridge

    def open(self):
        self.factory = ChatBridgeFactory("#skeetertoolingaround")
        reactor.connectTCP("irc.dhirc.com",6667,self.factory)
        self.factory.websocket = self

    def on_message(self, message):
        if message[0] != "/":
            self.irc_conn.say(self.factory.channel,message.encode('ascii','ignore'))
        self.write_message({"type":"chat", "user":"you", "message":message})

    def on_close(self):
        pass

if __name__ == "__main__":
    tornado.autoreload.start()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
