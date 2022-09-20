"""Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html

Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php
"""

################ Spelling Corrector 

import re
from collections import Counter

def words(text): return re.findall(r"\w+", text.lower())

def P(word):
  "Probability of `word`."
  return WORDS[word] / sum(WORDS.values())

def correct_norvig(word): 
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
  letters    = "abcdefghijklmnopqrstuvwxyz"
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

def spelltest(tests, correct_func, dictionary_ptr, verbose=False):
  "Run correction(wrong) on all (right, wrong) pairs; report results."
  import time
  start = time.time()
  good, unknown = 0, 0
  n = len(tests)
  for right, wrong in tests:
    w = correct_func(wrong)
    good += (w == right)
    if w != right:
      unknown += (right not in dictionary_ptr)
      if verbose:
        print("correction({}) => {} ({}); expected {} ({})".format(wrong, w, dictionary_ptr[w], right, dictionary_ptr[right]))
  dt = time.time() - start
  print("{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second".format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
  return [(right, wrong)
          for (right, wrongs) in (line.split(":") for line in lines)
          for wrong in wrongs.split()]

print("norvig")
WORDS = Counter(words(open("big.txt").read()))
spelltest(Testset(open("spell-testset1.txt")), correct_norvig, WORDS)
spelltest(Testset(open("spell-testset2.txt")), correct_norvig, WORDS)
print("norvig added data")
WORDS = Counter(words(open("big.txt").read()) + words(open("lemmas.txt").read()))
spelltest(Testset(open("spell-testset1.txt")), correct_norvig, WORDS)
spelltest(Testset(open("spell-testset2.txt")), correct_norvig, WORDS)

from symspellpy import SymSpell, Verbosity

def correct_symspell(word):
  suggestions_ptr = symspell_ptr.lookup(word, Verbosity.CLOSEST, max_edit_distance=EDIT_DISTANCE, include_unknown=True)
  return suggestions_ptr[0]._term

print("symspell")
EDIT_DISTANCE = 2
symspell_ptr = SymSpell(max_dictionary_edit_distance=EDIT_DISTANCE)
symspell_ptr.create_dictionary("big.txt")
spelltest(Testset(open("spell-testset1.txt")), correct_symspell, symspell_ptr.words)
spelltest(Testset(open("spell-testset2.txt")), correct_symspell, symspell_ptr.words)
print("symspell edits3")
EDIT_DISTANCE = 3
symspell_ptr = SymSpell(max_dictionary_edit_distance=EDIT_DISTANCE)
symspell_ptr.create_dictionary("big.txt")
spelltest(Testset(open("spell-testset1.txt")), correct_symspell, symspell_ptr.words)
spelltest(Testset(open("spell-testset2.txt")), correct_symspell, symspell_ptr.words)
print("symspell edits3 full data")
import pkg_resources
symspell_ptr = SymSpell(max_dictionary_edit_distance=EDIT_DISTANCE)
symspell_ptr.load_dictionary(pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt"), term_index=0, count_index=1)
spelltest(Testset(open("spell-testset1.txt")), correct_symspell, symspell_ptr.words)
spelltest(Testset(open("spell-testset2.txt")), correct_symspell, symspell_ptr.words)
