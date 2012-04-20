#
# A test script for the IndentStringBuilder.
#
# Output should look like the contents of guess.c,
# a little guessing game program.
#

INPUT_METHOD_BODY = \
"""int guess;

printf ("Guess: ");
scanf ("%d", &guess);

return guess;
"""

from indent.IndentWriter import *

sb = IndentStringBuilder ()

sb.println ('#include <stdio.h>')
sb.println ('#include <stdlib.h>')
sb.println ('#include <time.h>')

sb.newline ()

sb.println ('int main (int argc, char* argv[])')
sb.println ('{')

with sb:
   sb.println ('int target, guess;')
   sb.println ('srandom (time (NULL));');
   sb.newline ()
   sb.println ('target = random () % 100;')
   sb.newline ()
   sb.println ('while ((guess = input ()) != target) {')
   with sb:
      sb.println ('if (guess < target) {')
      with sb:
         sb.println ('printf ("Higher!\\n");')
      sb.println ('} else {')
      with sb:
         sb.println ('printf ("Lower!\\n");')
      sb.println ('}')
   sb.println ('}')
   sb.newline ()
   sb.println ('printf ("Winner!\\n");')
   sb.newline ()
   sb.println ('return 0;')
sb.println ('}')

sb.newline ()
sb.newline ()

sb.println ('int input ()')
sb.println ('{')

with sb:
   sb.printLines (INPUT_METHOD_BODY)

sb.println ('}')
sb.newline ()

sys.stdout.write (str (sb))
