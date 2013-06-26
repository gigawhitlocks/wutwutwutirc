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

    def open(self):
        pass

    def on_message(self, message):
        pass
                
    def on_close(self):
        pass

if __name__ == "__main__":
    tornado.autoreload.start()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
