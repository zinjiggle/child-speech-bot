# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = u'My name is Ji Zhu, I am from Beijing. I like US and I like China. Can you sing a song for me?'
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document)

print('Text: {}'.format(text))
print(sentiment)

entities = client.analyze_entities(document=document)
print(entities)

syntax = client.analyze_syntax(document)
print(syntax)
