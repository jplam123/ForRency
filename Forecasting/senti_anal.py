from textblob import TextBlob
from pandas import DataFrame


def textblob_anal(df):
    print("Hello there")
    blobs = [TextBlob(content) for content in df['text']]
    df['tb_Pol'] = [b.sentiment.polarity for b in blobs]
    df['tb_Subj'] = [b.sentiment.subjectivity for b in blobs]
