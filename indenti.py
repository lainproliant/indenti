#--------------------------------------------------------------------
# indent_tools.py: Tools for printing code strings,
#                        XML markup, and other indented text.
#
# Indent Tools is a module that simplifies the task of indenting output.
# It keeps track of indent levels and provides a pythonic way of incrementing
# and decrementing the indent level using the optional 'with' syntax.
#
# Makes clever use of the semantics of the Python 2.5+ "with"
# statement to allow indented generator code to indent along
# with its indented output.  This allows generator code to
# look much cleaner.
#
# (c) 2011-2016 Lee Supe (lain_proliant)
# Released under the GNU General Public License
#--------------------------------------------------------------------
import sys
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from itertools import repeat
from xml.sax.saxutils import escape as xml_escape
from xml.sax.saxutils import quoteattr as attr_escape

ELEMENT_NODE        = "Node"
ELEMENT_TEXT        = "Text"
ELEMENT_CDATA       = "CDATA"
ELEMENT_COMMENT     = "Comment"

# These HTML tags must omit their end tags.
HTML_VOID_TAGS = set(['area', 'base', 'br', 'col', 'hr', 'img', 'input',
                      'link', 'meta', 'param', 'command', 'keygen',
                      'source'])

# These tags should not be indented.
HTML_NOINDENT_TAGS = set(['textarea'])

#--------------------------------------------------------------------
class StringBuilder:
    """
        A simple string builder.  Collects an array of strings
        and concatenates them as effciently as possible.
    """

    def __init__(self, obj = None):
        self._strings = []

        if isinstance(obj, str):
            self.append(obj)

        elif isinstance(obj, list) or isinstance(obj, tuple):
            self.extend(obj)

    def get_lines(self):
        """
            Gets all of the individual lines of output.
        """

        lines = []

        for output_str in self._strings:
            lines.extend(filter(None, output_str.split('\n')))

        return lines

    def get_string(self):
        """
            Concatenates the list of output strings.

            This is much more efficient than concatenating
            on each write.
        """

        return ''.join(self._strings)

    def append(self, string):
        """
            Adds the given string.
        """

        self._strings.append(string)

    def extend(self, strings):
        """
            Adds the given list/tuple of strings.
        """

        map(self.append, strings)

    def __str__(self):
        return self.get_string()

#--------------------------------------------------------------------
class IndentBase:
    """
        An abstract base class for string indenting.
    """

    __metaclass__ = ABCMeta

    def __init__(self, outfile = sys.stdout):
        """
            Initializes an IndentWriter.
        """

        self._il = 0
        self._indent_str = '    '
        self._enabled = True
        self._isnewline = False

    @abstractmethod
    def _write_raw(self, output):
        """
            The raw write method.

            This method is private.

            This method is abstract and must be implemented
            by subclasses to pass on the output.
        """

        pass

    def __call__(self, output = None):
        """
            Called when the object is treated as a functor.
            This syntax is synonymous to calling println().

            EXAMPLE:

            iw = IndentWriter()
            iw("Hello,")
            iw.println("World!")

            OUTPUT:
            Hello,
            World!
        """

        if output is None:
            self.newline()
        else:
            self.println(output)

    def write(self, output):
        """
            Print the given line to output,
            indenting if necessary.
        """

        if self._isnewline:
            self._isnewline = False
            self._write_raw(self._indent_str * self._il)

        self._write_raw(output)

    def indent(self, level = 1):
        """
            Indent the given number of levels.

            A minimum indent level is not enforced
            by this method, though an indent level
            below zero is equivalent zero.
        """

        self._il += level

    def unindent(self, level = 1):
        """
            Unindent the given number of levels.

            The indent level cannot go below 0
            if this method is used to decrease
            the indent level.
        """

        self._il -= level

        if self._il < 0:
            self._il = 0

    def set_indent_string(self, indent_str):
        """
            Sets the string used to indent.

            This string is prepended to each line printed
            for each indent level.
        """

        self._indent_str = indent_str

    def set_enabled(self, enabled):
        """
            Sets whether indenting is enabled.
        """

        self._enabled = enabled

    def println(self, output):
        """
            Print the given line to output,
            indenting if necessary.

            A newline is appended to the output.
        """

        self.write(output)
        self.newline()

    def print_lines(self, output):
        """
            Prints the given string with multiple
            lines to output, indenting each line.
        """

        for line in output.splitlines():
            self.println(line)

    def writeln(self, output):
        """
            A synonym for println.
        """

        self.println(output)

    def newline(self):
        """
            Append a newline to the output.
        """

        self._isnewline = True
        self._write_raw('\n')

    def __enter__(self):
        """
            This method is called when the object enters
            the context of a with block.

            EXAMPLE:

            iw = IndentWriter()
            iw.println("Hello,")
            with iw:
                iw.println("World!")

            OUTPUT:

            Hello,
                World!
        """

        self.indent()

    def __exit__(self, exc_type, exc_val, exc_traceback):
        """
            This method is called when the object leaves
            the context of a with block.

            EXAMPLE:

            iw = IndentWriter()
            with iw:
                iw.println("Hello,")

            iw.println("World!")

            OUTPUT:

                Hello,
            World!
        """

        self.unindent()

#--------------------------------------------------------------------
class IndentWriter(IndentBase):
    """
        An indented text printer.

        Makes clever use of the semantics of the Python 2.5+ "with"
        statement to allow indented generator code to indent along
        with its indented output.  This allows generator code to
        look much cleaner.
    """

    def __init__(self, outfile = sys.stdout):
        """
            Initializes an IndentWriter.
        """

        IndentBase.__init__(self)

        self._outfile = outfile

    def _write_raw(self, output):
        """
            The raw write method.

            Sends the output on to the output file.
        """

        self._outfile.write(output)

#--------------------------------------------------------------------
class IndentStringBuilder(IndentBase, StringBuilder):
    """
        An indented string builder.

        Appends all of the given input into a string,
        which can be fetched via str() or via
        IndentStringBuilder.get_string().
    """

    def __init__(self):
        """
            Initializes an IndentStringBuilder.
        """

        IndentBase.__init__(self)
        StringBuilder.__init__(self)

    def _write_raw(self, output):
        """
            The raw write method.

            Adds the given output string to a list of strings
            to be concatenated when necessary.
        """

        self.append(output)

#--------------------------------------------------------------------
class XmlElementBase:
    __metaclass__ = ABCMeta

    def __init__(self, node_type):
        self._node_type = node_type

    @property
    def nodetype(self):
        return self._node_type

#--------------------------------------------------------------------
class TextObject:
    """
        An interface for objects which are transformed into text.
        This allows certain types of behavior such as
        interpolations and translation subsitutions to happen
        while the Xml/Html document is being rendered.
    """
    def __str__(self):
        raise NotImplementedError()

#--------------------------------------------------------------------
class XmlText(XmlElementBase):
    """
        A node containing text.
    """

    def __init__(self, text):
        XmlElementBase.__init__(self, ELEMENT_TEXT)
        self._text = text

    def __str__(self):
        return xml_escape(str(self._text))

#--------------------------------------------------------------------
class XmlElement(XmlElementBase):
    """
        A class representing an xml element, or node.
        This element can have text, child elements, and attributes.

        This element is created by XmlFactory dynamically.
    """

    def __init__(self, name, attrs = None, html = False):
        XmlElementBase.__init__(self, ELEMENT_NODE)
        self._name = name
        self._doctype = None
        self._html = html

        self._children = []

        if attrs is None:
            self._attrs = OrderedDict()
        else:
            self._attrs = OrderedDict(attrs)

    def doctype(self, doctype):
        self._doctype = doctype
        return self

    def append(self, child):
        if self._html and self._name in HTML_VOID_TAGS:
            raise ValueError('HTML void tags (%s) cannot have child elements.' % (
                ', '.join(HTML_VOID_TAGS)))
        self._children.append(child)
        return self

    def apply(self, *args, **kwargs):
        """
            Applies the given elements and/or attributes.
        """

        if kwargs is not None:
            self._attrs.update(kwargs)

        for child in args:
            if isinstance(child, str) or isinstance(child, TextObject):
                self.append(XmlText(child))
            elif isinstance(child, list) or isinstance(child, tuple):
                self.apply(*child)
            elif(isinstance(child, dict)):
                for key, value in child.items():
                    if key == 'class' and self._html and 'class' in self._attrs:
                        self._attrs['class'] += ' ' + value
                    else:
                        self._attrs[key] = value
            else:
                self.append(child)

        return self

    def _get_attrs_str(self):
        attr_decls = []

        for attr, value in self._attrs.items():
            if value is not None:
                attr_decls.append('%s=%s' % (xml_escape(attr), attr_escape(str(value))))
            else:
                attr_decls.append('%s' % xml_escape(attr))

        return ' '.join(attr_decls)

    def __str__(self):
        """
            Constructs a string representation of the xml
            element and it's child elements.
        """

        sb = IndentStringBuilder()

        if self._doctype is not None:
             sb("<!doctype %s>" % self._doctype)

        if not self._children:
            if self._html and self._name not in HTML_VOID_TAGS:
                if not self._attrs:
                    sb("<%s></%s>" % (xml_escape(self._name), xml_escape(self._name)))
                else:
                    sb("<%s %s></%s>" % (xml_escape(self._name), self._get_attrs_str(),
                                         xml_escape(self._name)))
            elif not self._attrs:
                sb("<%s/>" % (xml_escape(self._name)))
            else:
                sb("<%s %s/>" % (xml_escape(self._name), self._get_attrs_str()))

        else:
            if self._html and self._name in HTML_NOINDENT_TAGS:
                if not self._attrs:
                    sb("<%s>%s</%s>" % (
                        xml_escape(self._name),
                        ''.join(str(child) for child in self._children),
                        xml_escape(self._name)))
                else:
                    sb("<%s %s>%s</%s>" % (
                        xml_escape(self._name),
                        self._get_attrs_str(),
                        ''.join(str(child) for child in self._children),
                        xml_escape(self._name)))

            else:
                if not self._attrs:
                    sb("<%s>" % (xml_escape(self._name)))
                else:
                    sb("<%s %s>" % (xml_escape(self._name), self._get_attrs_str()))

                with sb:
                    for child in self._children:
                        sb.print_lines(str(child))

                sb("</%s>" % xml_escape(self._name))

        return str(sb)

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

#--------------------------------------------------------------------
class XmlFactory:
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

    def __init__(self, html = False):
         self.__html = html

    def __getattr__(self, element_name):
        """
            Creates a callable XmlFunctor for the given element name.
            If you need an element with a name which is not a valid
            python variable name(i.e., "1stName"), call this method
            directly, i.e.:

            xf.__getattr__("1stName")("Lee")
        """

        return XmlFunctor(element_name, html = self.__html)

#--------------------------------------------------------------------
class HtmlFactory(XmlFactory):
    """
        A factory to create XmlElement objects.
        Supports a dynamic attribute pattern to instantiate these
        objects as well as set properties and add children.

        Additionally, the HtmlFactory generates XmlElement elements
        that conform to HTML5 (e.g., void tags can't have child elements,
        non-void tags always have closing tags).
    """

    def __init__(self):
        super().__init__(html = True)

#--------------------------------------------------------------------
class XmlFunctor:
    """
        A functor used by XmlFactory to offer a dynamic way to
        construct XmlElements.
    """

    def __init__(self, element_name, html = False):
        self._element_name = element_name
        self._html = html

    def __call__(self, *args, **kwargs):
        """
            The dynamic constructor for XmlFactory.
            Creates an XmlElement of the type specified
            in the attribute name from XmlFactory.
        """

        node = XmlElement(self._element_name, html = self._html)
        node.apply(*args, **kwargs)

        return node

#--------------------------------------------------------------------
# Define a global XmlFactory for modules to use.
xml = HtmlFactory()

#--------------------------------------------------------------------
# Define a global HtmlFactory for modules to use.
html = HtmlFactory()
