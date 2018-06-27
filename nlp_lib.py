# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
CLIENT = language.LanguageServiceClient()

# # The text to analyze
# text = u'My name is Ji Zhu, I am from Beijing. I like US and I like China. Can you sing a song for me?'
# document = types.Document(
#     content=text,
#     type=enums.Document.Type.PLAIN_TEXT)

# print('Text: {}'.format(text))
# print(sentiment)

# entities = client.analyze_entities(document=document)
# print(entities)

# syntax = client.analyze_syntax(document)
# print(syntax)


class EnglishAnalyzeProcessorBase(object):
  """Base class to analyze English the return response."""

  def get_response(self, text, entity_response, syntax_response):
    """Get response by analyzing entity response and syntax response.

    entity_response: types.AnalyzeEntitiesResponse
    syntax_response: types.AnalyzeSyntaxResponse

    returns None if this is not the correct class to handle the input.
    """
    return None


class SayHelloProcessor(EnglishAnalyzeProcessorBase):

  def get_response(self, text, entity_response, syntax_response):
    if 'hello' in text:
      return 'hello'
    if 'hi' in text:
      return 'Hi, let us be friends!'
    return None


class AskNameProcessor(EnglishAnalyzeProcessorBase):

  def get_response(self, text, entity_response, syntax_response):
    if 'what' in text and 'name' in text:
      return 'You can call me lucky, maybe we can play together.'
    return None


class AskToSingSongProcessor(EnglishAnalyzeProcessorBase):

  def get_response(self, text, entity_response, syntax_response):
    if 'sing' in text and 'song' in text:
      return 'Which song do you like?'
    return None


class WhatICanDoProcessor(EnglishAnalyzeProcessorBase):

  def get_response(self, text, entity_response, syntax_response):
    if 'what' in text and 'can do' in text and 'you' in text:
      return 'I can do a lot of things, like singing, dancing, playing games.'
    return None


def NlpTextHandler(text):
  processors = [SayHelloProcessor(),
                AskNameProcessor(),
                AskToSingSongProcessor(),
                WhatICanDoProcessor()]
  for proc in processors:
    res = proc.get_response(text, None, None)
    if res:
      return res
  return 'I do not understand, sorry.'
