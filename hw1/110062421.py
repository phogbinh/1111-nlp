"""Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html

Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php
"""

################ Spelling Corrector 

import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

def P(word):
  "Probability of `word`."
  return WORDS[word] / sum(WORDS.values())

def correction(word): 
  "Most probable spelling correction for word."
  return max(candidates(word), key=P)

def candidates(word): 
  "Generate possible spelling corrections for word."
  return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
  "The subset of `words` that appear in the dictionary of WORDS."
  return set(w for w in words if w in WORDS)

def edits1(word):
  "All edits that are one edit away from `word`."
  letters    = 'abcdefghijklmnopqrstuvwxyz'
  splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
  deletes    = [L + R[1:]               for L, R in splits if R]
  transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
  replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
  inserts    = [L + c + R               for L, R in splits for c in letters]
  return set(deletes + transposes + replaces + inserts)

def edits2(word): 
  "All edits that are two edits away from `word`."
  return (e2 for e1 in edits1(word) for e2 in edits1(e1))

################ Test Code 

def spelltest(tests, verbose=False):
  "Run correction(wrong) on all (right, wrong) pairs; report results."
  import time
  start = time.time()
  good, unknown = 0, 0
  n = len(tests)
  for right, wrong in tests:
    w = correction(wrong)
    good += (w == right)
    if w != right:
      unknown += (right not in WORDS)
      if verbose:
        print('correction({}) => {} ({}); expected {} ({})'.format(wrong, w, WORDS[w], right, WORDS[right]))
  dt = time.time() - start
  print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second'.format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
  "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
  return [(right, wrong)
          for (right, wrongs) in (line.split(':') for line in lines)
          for wrong in wrongs.split()]

WORDS = Counter(words(open('big.txt').read()) + words(open('lemmas.txt').read()))
spelltest(Testset(open('spell-testset1.txt')))
spelltest(Testset(open('spell-testset2.txt')))
