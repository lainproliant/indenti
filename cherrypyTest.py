import cherrypy
from indent.XmlWriter import *

class HelloWorld:
    @cherrypy.expose
    def index (self):
        xf = XmlFactory ()

        xml = xf.html (
        xf.head (
            xf.title ("Hello, world!")),
                xf.body (
                    xf.h1 ("Hello, CherryPy!", style='color: red; font-size: 20px')))
        
        xml.doctype = 'html'
        return str(xml)

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
