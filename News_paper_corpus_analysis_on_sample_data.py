
import nltk
import string
import re
import pandas as pd
from nltk.corpus import stopwords
import numpy as np
from os import path
from PIL import Image
import matplotlib.pyplot as plt

list_of_punctuations = string.punctuation

list_of_english_stopwords = stopwords.words('english')

pd.set_option('display.max_colwidth', 100)

# There are 179 English Stopwords in NLTK

print(f'Number of english stopwords {len(list_of_english_stopwords)}')
print(f'Number of english punctuations {len(list_of_punctuations)}')






business_data_raw_text = pd.read_csv('Random_Sample_Data_Business_Single.txt', sep="\t",encoding='cp1252', names=['raw_text'])
business_data_raw_text.head()




## Remove Punctuations from text

def remove_punctuation(text):
    text_without_punctuation = "".join([char for char in text if char not in list_of_punctuations])
    return text_without_punctuation

business_data_raw_text['remove_punctuations'] = business_data_raw_text['raw_text'].apply(lambda x: remove_punctuation(x))
business_data_raw_text.head()




# Perform Tokenization on the text

def tokenize(text):
    tokens = re.split('\W+', text)
    return tokens

business_data_raw_text['tokenize_text'] = business_data_raw_text['remove_punctuations'].apply(lambda x: tokenize(x.lower()))
business_data_raw_text.head()




# Removing Stop Words from the text

def remove_stopwords(tokenized_list):
    token_without_stopwords = [word for word in tokenized_list if word not in list_of_english_stopwords]
    return token_without_stopwords

business_data_raw_text['removed_stop_words'] = business_data_raw_text['tokenize_text'].apply(lambda x: remove_stopwords(x))

business_data_raw_text.head()



# Perform Stemming : Process of reducing inflected (or sometimes derived) words to their word stem or root

ps = nltk.PorterStemmer()

def stemmer(removed_stop_words):
    text = [ps.stem(word) for word in removed_stop_words]
    return text

business_data_raw_text['stemmed_words'] = business_data_raw_text['removed_stop_words'].apply(lambda x: stemmer(x))

business_data_raw_text.head()




#Lemmatization as stemming is as accurate as it should be being that it doesn't try to understand
#the context of the words before trimming to its root words. It's advantage is being faster because it doesn't have 
# to check these contexts. 

wn = nltk.WordNetLemmatizer()

def Lemmatize(removed_stop_words):
    text = [wn.lemmatize(word) for word in removed_stop_words]
    return text

business_data_raw_text['lemmetized_words'] = business_data_raw_text['removed_stop_words'].apply(lambda x: Lemmatize(x))

business_data_raw_text.head(50)



business_data_raw_text.head(50)
print(50)




# Generate Word Cloud

# Start with loading all necessary libraries

get_ipython().run_line_magic('matplotlib', 'inline')







#?WordCloud
text = ""
#join all the words, preferably the
for lem_word in business_data_raw_text['lemmetized_words']:
    for word in lem_word:
        text = text + " " + word
    
#text  = business_data_raw_text['lemmetized_words']

wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)

plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# Save the image:
#wordcloud.to_file("first_review.png")









