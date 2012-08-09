#
# IndentWriter
#
# An indented text printer.
#
# Makes clever use of the semantics of the Python 2.5+ "with"
# statement to allow indented generator code to indent along 
# with its indented output.  This allows generator code to 
# look much cleaner.
#
# (c) 2011 Lee Supe (lain_proliant)
# Released under the GNU General Public License
#

import sys
from abc import ABCMeta, abstractmethod

from indent.StringBuilder import StringBuilder

#--------------------------------------------------------------------
class IndentBase (object):
   """
      An abstract base class for string indenting.
   """

   __metaclass__ = ABCMeta
   
   def __init__ (self, outfile = sys.stdout):
      """
         Initializes an IndentWriter.
      """

      self.il = 0
      self.indentStr = '   '
      self.enabled = True
      self.isnewline = False

   
   @abstractmethod
   def _write_raw (self, output):
      """
         The raw write method.

         This method is private.

         This method is abstract and must be implemented
         by subclasses to pass on the output.
      """
      
      pass


   def __call__ (self, output = None):
      """
         Called when the object is treated as a functor.
         This syntax is synonymous to calling println ().

         EXAMPLE:

         iw = IndentWriter ()
         iw ("Hello,")
         iw.println ("World!")

         OUTPUT:
         Hello,
         World!
      """
      
      if output is None:
         self.newline ()
      else:
         self.println (output)


   def write (self, output):
      """
         Print the given line to output,
         indenting if necessary.
      """

      if self.isnewline:
         self.isnewline = False
         self._write_raw (self.indentStr * self.il)

      self._write_raw (output)


   def indent (self, level = 1):
      """
         Indent the given number of levels.

         A minimum indent level is not enforced
         by this method, though an indent level
         below zero is equivalent zero.
      """

      self.il += level

   
   def unindent (self, level = 1):
      """
         Unindent the given number of levels.

         The indent level cannot go below 0
         if this method is used to decrease
         the indent level.
      """
      
      self.il -= level

      if self.il < 0:
         self.il = 0


   def setIndentString (self, indentStr):
      """
         Sets the string used to indent.

         This string is prepended to each line printed
         for each indent level.
      """

      self.indentStr = indentStr


   def setEnabled (self, enabled):
      """
         Sets whether indenting is enabled.
      """

      self.enabled = enabled


   def println (self, output):
      """
         Print the given line to output,
         indenting if necessary.

         A newline is appended to the output.
      """
      
      self.write (output)
      self.newline ()


   def printLines (self, output):
      """
         Prints the given string with multiple
         lines to output, indenting each line.
      """
      
      for line in output.splitlines ():
         self.println (line)


   def writeln (self, output):
      """
         A synonym for println.
      """

      self.println (output)


   def newline (self):
      """
         Append a newline to the output.
      """

      self.isnewline = True
      self._write_raw ('\n')


   def __enter__ (self):
      """
         This method is called when the object enters
         the context of a with block.

         EXAMPLE:

         iw = IndentWriter ()
         iw.println ("Hello,")
         with iw:
            iw.println ("World!")

         OUTPUT:

         Hello,
            World!
      """
      
      self.indent ()

   
   def __exit__ (self, excType, excVal, excTraceback):
      """
         This method is called when the object leaves
         the context of a with block.

         EXAMPLE:

         iw = IndentWriter ()
         with iw:
            iw.println ("Hello,")

         iw.println ("World!")

         OUTPUT:

            Hello,
         World!
      """

      self.unindent ()
   
#--------------------------------------------------------------------
class IndentWriter (IndentBase):
   """
      An indented text printer.
   """

   def __init__ (self, outfile = sys.stdout):
      """
         Initializes an IndentWriter.
      """
      
      IndentBase.__init__ (self)

      self.outfile = outfile

   
   def _write_raw (self, output):
      """
         The raw write method.

         Sends the output on to the output file.
      """
      
      self.outfile.write (output)

#--------------------------------------------------------------------
class IndentStringBuilder (IndentBase, StringBuilder):
   """
      An indented string builder.

      Appends all of the given input into a string,
      which can be fetched via str () or via
      IndentStringBuilder.getString ().
   """

   def __init__ (self):
      """
         Initializes an IndentStringBuilder.
      """
      
      IndentBase.__init__ (self)
      StringBuilder.__init__ (self)
   

   def _write_raw (self, output):
      """
         The raw write method.

         Adds the given output string to a list of strings
         to be concatenated when necessary.
      """

      self.append (output)

   

