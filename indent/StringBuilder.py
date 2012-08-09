#
# StringBuilder
#
# A simple string builder.  Collects an array of strings
# and concatenates them as effciently as possible.
#
# (c) April 2012 Lee Supe (lain_proliant)
# Released under the GNU General Public License
#

import sys

#--------------------------------------------------------------------
class StringBuilder (object):
   """
      A simple string builder.
   """

   def __init__ (self, obj = None):
      self.strings = []

      if isinstance (obj, str):
         self.append (obj)

      elif isinstance (obj, list) or isinstance (obj, tuple):
         self.extend (obj)
   

   def getLines (self):
      """
         Gets all of the individual lines of output.
      """
      
      lines = []

      for outputStr in self.strings:
         lines.extend (filter (None, outputStr.split ('\n')))
      
      return lines


   def getString (self):
      """
         Concatenates the list of output strings.

         This is much more efficient than concatenating
         on each write.
      """

      return ''.join (self.strings)

   
   def append (self, string):
      """
         Adds the given string.
      """

      self.strings.append (string)

   
   def extend (self, strings):
      """
         Adds the given list/tuple of strings.
      """

      map (self.append, strings)


   def __str__ (self):
      return self.getString ()


