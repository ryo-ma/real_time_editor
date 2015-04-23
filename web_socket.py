import sys
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

ws_list = set()

f = open("./index.html")
content = f.read()
f.close()

def app(environ, start_response):
    if environ["PATH_INFO"] == '/echo':
        ws = environ["wsgi.websocket"]
        ws_list.add(ws)
        print str(len(ws_list)) + "enter"
        while True:
            message = ws.receive()
            print message
            if message is None:
                break
            for s in ws_list:
            	s.send(message)
    else:
        start_response("200 OK", [
                ("Content-Type", "text/html"),
                ("Content-Length", str(len(content)))
                ])  
        return iter([content])

if __name__=="__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()