About Indent Tools
========================

Indent Tools is a Python package with tools that make string building,
writing indented text, and generating markup easier and prettier.

Indent Tools contains the following modules:

   * IndentWriter
   * XmlWriter
   * StringBuilder

# About IndentWriter
IndentWriter is a module that simplifies the task of indenting output.
It keeps track of indent levels and provides a pythonic way of incrementing
and decrementing the indent level using the optional 'with' syntax.
By default, IndentWriter writes to sys.stdout, but can be told to write to
any other File object at construction.


Example Usage, IndentWriter(using 'with'):

```
from indent.IndentWriter import *

iw = IndentWriter()

iw('def hello():')
with iw:
    iw('print "Hello!"')
```

Example Usage, IndentWriter(without 'with'):
```
from indent.IndentWriter import *

iw = IndentWriter()
iw('def hello():')
iw.indent()
iw('print "Hello!"')
```

Example Usage, IndentStringBuilder:
```
from indent.IndentWriter import *

sb = IndentStringBuilder()

sb('def hello():')
with sb:
    sb('print "Hello!"')

print str(sb)
```

# About XmlWriter 
XmlWriter is a python module that facilitates the generation of
XML markup.  Via XmlFactory, any node name can be specified as
an attribute, which returns a functor to create a new node.

Example Usage, XmlWriter(A CherryPy HTML Servlet):
```
import cherrypy
from indent.XmlWriter import *

class HelloWorld:
    def index(self):
        xf = XmlFactory()

        xml = xf.html(
        xf.head(
            xf.title("Hello, world!")),
                xf.body(
                    xf.h1("Hello, CherryPy!", style='color: red; font-size: 20px')))
      
        return str(xml)

    index.exposed = True
```
### NOTE:
The word 'class' is a python keyword, so we can't use it as a keyword argument
to create an attribute name.  In this case, we pass a dictionary, which
is interpreted as a map of attributes for the node.  You can always do this
instead of using keyword arguments, if this is your preference.

Example Usage, XmlWriter(Using attributes/nodes that conflict with python keywords):
```
    import cherrypy
    from indent.XmlWriter import *

    class HelloWorld:
       def index(self):
          xf = XmlFactory()

          xml = xf.html(
                xf.head(
                   xf.title("Hello, world!")),
                xf.body(
                   xf.h1("Hello, CherryPy!", {'class': 'header')))
      
          return str(xml)

       index.exposed = True
```

# About StringBuilder
StringBuilder is a simple class that builds a string from a list of strings.
In function, it is similar to java.lang.StringBuilder from Java, but it
includes a bit more functionality that is useful for markup generation.

Example Usage, StringBuilder(from XmlWriter.XmlElement.getString()):
```
    def getString(self):
       """
          Constructs a string representation of the xml
          element and it's child elements.
       """

       sb = IndentStringBuilder()
      
       if not self.children:
          if not self.attrs:
             sb("<%s/>" %(xml_escape(self.name)))
          else:
             sb("<%s %s/>" %(xml_escape(self.name), self._getAttrsStr()))
 
       else:
          if not self.attrs:
             sb("<%s>" %(xml_escape(self.name)))
          else:
             sb("<%s %s>" %(xml_escape(self.name), self._getAttrsStr()))
 
          with sb:
             for child in self.children:
                sb.printLines(str(child))
 
          sb("</%s>" % xml_escape(self.name))
 
       return str(sb)
```
