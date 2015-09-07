#
# XmlWriter
#
# A python module to generate and manipulate XML markup.
#
# (c) April 2012 Lee Supe (lain_proliant)
# Released under the GNU General Public License
#

import sys
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from indent.StringBuilder import StringBuilder
from indent.IndentWriter import *

from xml.sax.saxutils import escape as xml_escape

ELEMENT_NODE      = "Node"
ELEMENT_TEXT      = "Text"
ELEMENT_CDATA     = "CDATA"
ELEMENT_COMMENT   = "Comment"

#--------------------------------------------------------------------
class XmlElementBase(object):
   
   __metaclass__ = ABCMeta

   def __init__(self, nodeType):
      self.nodeType = nodeType

   @property
   def nodetype(self):
      return self.nodeType

#--------------------------------------------------------------------
class XmlText(XmlElementBase):
   """
      A node containing text.
   """

   def __init__(self, text):
      self.text = text

   def __str__(self):
      return xml_escape(self.text)


#--------------------------------------------------------------------
class XmlElement(XmlElementBase):
   """
      A class representing an xml element, or node.  
      This element can have text, child elements, and attributes.
      
      This element is created by XmlFactory dynamically.
   """
   
   def __init__(self, name, attrs = None):
      XmlElementBase.__init__(self, ELEMENT_NODE)
      self.name = name
      self.doctype = None

      self.children = []

      if attrs is None:
         self.attrs = OrderedDict()
      else:
         self.attrs = OrderedDict(attrs)
   
   
   def apply(self, *args, **kwargs):
      """
         Applies the given elements and/or attributes.
      """
      
      if kwargs is not None:
         self.attrs.update(kwargs)

      for child in args:
         if isinstance(child, str):
            self.children.append(XmlText(child))
         elif isinstance(child, list) or isinstance(child, tuple):
            self.apply(*child)
         elif(isinstance(child, dict)):
            self.attrs.update(child)
         else:
            self.children.append(child)


   def __str__(self):
      return self.getString() 


   def getString(self):
      """
         Constructs a string representation of the xml
         element and it's child elements.
      """

      sb = IndentStringBuilder()
        
      if self.doctype is not None:
          sb("<!doctype %s>" % self.doctype)

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


   def _getAttrsStr(self):
      return ' '.join(['%s="%s"' % tuple(map(xml_escape, x)) for x in \
            self.attrs.items()])
   
   def __call__(self, *args, **kwargs):
      self.apply(args, kwargs)


#--------------------------------------------------------------------
class XmlFactory(object):
   """
      A factory to create XmlElement objects.
      Supports a dynamic attribute pattern to instantiate these
      objects as well as set properties and add children.

      EXAMPLE:
         
         x = XmlFactory()
         html = x.html(x.head(x.title("Title")),
            x.body(x.h1("Hello, world!", style="color: red;")))
         print(html)
   """

   def __init__(self):

      pass


   def __getattr__(self, elementName):
      """
         Creates a callable XmlFunctor for the given element name.
         If you need an element with a name which is not a valid
         python variable name(i.e., "1stName"), call this method
         directly, i.e.:

         xf.__getattr__("1stName")("Lee")
      """

      return XmlFunctor(elementName)


#--------------------------------------------------------------------
class XmlFunctor(object):
   """
      A functor used by XmlFactory to offer a dynamic way to
      construct XmlElements.
   """
   
   def __init__(self, elementName):
      self.elementName = elementName


   def __call__(self, *args, **kwargs):
      """
         The dynamic constructor for XmlFactory.
         Creates an XmlElement of the type specified
         in the attribute name from XmlFactory.
      """
      
      node = XmlElement(self.elementName)
      node.apply(*args, **kwargs)

      return node
