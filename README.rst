About Indenti
==================

Indenti is a Python package with tools that make string building,
writing indented text, and generating markup easier and prettier.

Indenti contains the following modules:

-  IndentWriter
-  XmlWriter
-  StringBuilder

Installation
------------

Installation is simple. With python3-pip, do the following:

$ sudo pip install -e .

About IndentWriter
==================

IndentWriter is a module that simplifies the task of indenting output.
It keeps track of indent levels and provides a pythonic way of
incrementing and decrementing the indent level using the optional 'with'
syntax. By default, IndentWriter writes to sys.stdout, but can be told
to write to any other File object at construction.

Example Usage, IndentWriter(using 'with'):

::

    from indenti import IndentWriter

    iw = IndentWriter()

    iw('def hello():')
    with iw:
        iw('print "Hello!"')

Example Usage, IndentWriter(without 'with'):

::

    from indenti import IndentWriter

    iw = IndentWriter()
    iw('def hello():')
    iw.indent()
    iw('print "Hello!"')

Example Usage, IndentStringBuilder:

::

    from indenti import IndentStringBuilder

    sb = IndentStringBuilder()

    sb('def hello():')
    with sb:
        sb('print "Hello!"')

    print str(sb)

About XmlFactory
================

Via XmlFactory, any node name can be specified as an attribute, which
returns a functor to create a new node.

Example Usage, XmlWriter(A CherryPy HTML Servlet):

::

    import cherrypy
    from indenti import XmlFactory

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

NOTE:
~~~~~

The word 'class' is a python keyword, so we can't use it as a keyword
argument to create an attribute name. In this case, we pass a
dictionary, which is interpreted as a map of attributes for the node.
You can always do this instead of using keyword arguments, if this is
your preference.

Example Usage, XmlWriter(Using attributes/nodes that conflict with
python keywords):

::

        import cherrypy
        from indenti import XmlFactory

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

Change Log
----------

Version 1.4: April 22nd, 2017
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Make XmlFactory callable, allowing tags with dashes, e.g. xf('my-dash-tag')()

Version 1.2: November 1st, 2016
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Make parents respect the NOINDENT status of their children in HTML mode.

Version 1.1: October 18th, 2016
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Added support for unindented blocks in HTML mode (for textarea)
- Fixed escaping of XML attributes


