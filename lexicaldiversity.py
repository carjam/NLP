#!/usr/local/bin/python3
from textutility import TextUtility
from math import log

from nltk.stem.porter import PorterStemmer
from itertools import groupby

class LexicalDiversity(object):
  def __init__(self,text):
    self.__text = text.lower().strip()

  
  # Function to compute the base-2 logarithm of a floating point number.
  def __log2(self,number):
    return log(number) / log(2)


  def calcCharEntropy(self):
    letter_frequency = TextUtility.countLetterFrequencies(self.__text)
    length_sum = 0.0
    for letter in letter_frequency:
      probability = float(letter_frequency[letter]) / sum(letter_frequency.values())
      length_sum -= probability * self.__log2(probability)
    return length_sum


  def calcWordEntropy(self):
    word_frequency = TextUtility.countWordFrequencies(self.__text)
    length_sum = 0.0
    for word in word_frequency.keys():
      probability = float(word_frequency[word]) / sum(word_frequency.values())
      length_sum -= probability * self.__log2(probability)
    return length_sum

  
  def yulei(self):
    # yule's I measure (the inverse of yule's K measure)
    # higher number is higher diversity - richer vocabulary
    d = {}
    stemmer = PorterStemmer()
    words = TextUtility.tokenizeText(self.__text)
    for w in words:
      w = stemmer.stem(w).lower()
      try:
        d[w] += 1
      except KeyError:
        d[w] = 1
 
    M1 = float(len(d))
    M2 = sum([len(list(g))*(freq**2) for freq,g in groupby(sorted(d.values()))])

    try:
      return (M1*M1)/(M2-M1)
    except ZeroDivisionError:
      return 0

