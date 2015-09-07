#
# A test script for the IndentWriter.
#
# Output should look like the contents of guess.c,
# a little guessing game program.
#

from indent.IndentWriter import *

iw = IndentWriter()

iw('#include <stdio.h>')
iw('#include <stdlib.h>')
iw('#include <time.h>')

iw.newline()

iw('int main(int argc, char* argv[])')
iw('{')

with iw:
   iw('int target, guess;')
   iw('srandom(time(NULL));');
   iw.newline()
   iw('target = random() % 100;')
   iw.newline()
   iw('while((guess = input()) != target) {')
   with iw:
      iw('if(guess < target) {')
      with iw:
         iw('printf("Higher!\\n");')
      iw('} else {')
      with iw:
         iw('printf("Lower!\\n");')
      iw('}')
   iw('}')
   iw.newline()
   iw('printf("Winner!\\n");')
   iw.newline()
   iw('return 0;')
iw('}')

iw.newline()
iw.newline()

iw('int input()')
iw('{')
with iw:
   iw('int guess;')
   iw.newline()
   iw('printf("Guess: ");')
   iw('scanf("%d", &guess);')
   iw.newline()
   iw('return guess;')
iw('}')
iw.newline()




