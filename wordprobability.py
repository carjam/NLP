#!/usr/local/bin/python3
from textutility import TextUtility
import re
import numpy
from memoized import memoized


class WordProbability(object):
  def __init__(self,text):
    self.__text = text.lower().strip()

  
  def __is_number(self,s):
    try:
        float(s)
        return True
    except ValueError:
        return False


  '''Word Probability'''
  @memoized
  def __calculateWordProbabilities(self):
    word_frequency = TextUtility.countWordFrequencies(self.__text) #language depedent
    word_count = TextUtility.countWords(self.__text)

    MIN_CHARS = 5
    regexp = "[A-Za-z]+"
    exp = re.compile(regexp)
    for k, v in list(word_frequency.items()):
      if not(exp.match(k)):
        del word_frequency[k]

    word_probabilities = {}
    for word in word_frequency.keys():
      if len(word) >= MIN_CHARS:
        word_probabilities[word] = float(word_frequency[word] / word_count) 

    return word_probabilities.items()


  #extract words with high information
  def probableWords(self,percentile):
    word_probabilities = dict(self.__calculateWordProbabilities())

    probabilities = list(word_probabilities.values())
    percentile_score = numpy.percentile(probabilities,percentile,axis=0, interpolation='lower')
    
    highinfo_words = []
    word_probabilities = dict(sorted(word_probabilities.items(), key=lambda k: k[1], reverse=True))
    for word in word_probabilities:
      probability = word_probabilities[word]
      if self.__is_number(probability) and probability > 0 :
        if percentile_score >= float(probability):
          highinfo_words.append(word) 

    return set(highinfo_words)


  #extract words with low information
  def unlikelyWords(self,percentile):
    word_probabilities = dict(self.__calculateWordProbabilities())

    probabilities = list(word_probabilities.values())
    percentile_score = numpy.percentile(probabilities,percentile,axis=0, interpolation='lower')
    
    lowinfo_words = []
    word_probabilities = dict(sorted(word_probabilities.items(), key=lambda k: k[1], reverse=True))
    for word in word_probabilities:
      probability = word_probabilities[word]
      if self.__is_number(probability) and probability > 0 :
        if percentile_score < float(probability):
          lowinfo_words.append(word) 

    return set(lowinfo_words)

 
  def hashtagSuggestions(self,percentile):
    hashtags = list(self.unlikelyWords(percentile))
    hashtags[:] = ['#' + word for word in hashtags]
    return hashtags


  def summary(self,percentile):
    sentences = TextUtility.sentenceTokenizeText(self.__text)
    words = self.unlikelyWords(percentile)
    result=[]
    for sentence in sentences:
      word_match = 0
      for word in words:
        if word in sentence:
          word_match += 1
          if word_match > 2 and len(sentence) < 150 and sentence not in result:
            result.append(sentence)
    
    if len(result) == 0:
      result.append('None available')
    return result
