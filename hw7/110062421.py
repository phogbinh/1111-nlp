import streamlit as st
from symspellpy import SymSpell, Verbosity
import pkg_resources

if "symspell" not in st.session_state:
  st.session_state["symspell"] = SymSpell(max_dictionary_edit_distance=3)
  st.session_state["symspell"].load_dictionary(pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt"), term_index=0, count_index=1)
checkbox = st.sidebar.checkbox("Show original word")
st.title("Spellchecker Demo")
selection = st.selectbox("Choose a word or...", ("", "apple", "lamon", "speling", "hapy", "language", "greay", "sussess"))
word = st.text_input("type your own!!!")
if selection != "":
  word = selection
if checkbox:
  st.write("Original word: " + word)
correct_word = st.session_state["symspell"].lookup(word, Verbosity.CLOSEST, max_edit_distance=3, include_unknown=True)[0]._term
if word != "":
  if correct_word == word:
    st.success(word + " is the correct spelling!")
  else:
    st.error("Correction: " + correct_word)
