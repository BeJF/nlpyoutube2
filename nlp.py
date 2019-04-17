from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import nltk
#nltk.download("punkt")

#ps = PorterStemmer()

def contain_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

# Each comment is tokenized. We have a list of list of words. We filter out the stopwords in the same time.
# => what to do with comments with multiple sentences?
def filter_tokenize(comments) :
    #could add stemming
    comments_tokenized = []
    for comment in comments :
        tokenized = word_tokenize(comment)
        filtered = [w.lower() for w in tokenized if not w.lower() in stop_words and w.isalpha()]
        comments_tokenized.append(filtered)
    return (comments_tokenized)
    
def list_words(sentences):
    words = []
    for sentence in sentences :
        for word in sentence :
            words.append(word)
    return (words)

def get_common_words(comments, nb_words) :
    words = list_words(comments)
    distribution = nltk.FreqDist(words)
    print("Words distribution = \n", distribution.most_common(nb_words), "\n")
    most_common = [w[0] for w in distribution.most_common(nb_words)]
    return (most_common)

# Doesnt work the same if tokenized or not. Token: camera. No tokens: camera + cameraman. Stemming would change that.
def find_comments(include, exclude, comments) :
    usefull_comments = []
    for comment in comments :
        if all(inc in comment for inc in include):
            if all(exc not in comment for exc in exclude):
                usefull_comments.append(comment)
    return (usefull_comments)

def print_list(list) :
    i = 0
    for item in list :
        i += 1
        print(i,":",item)

# Open the file with comments and store it in a list of string.
with open("comments.txt", "r") as f :
    all_comments=f.read().splitlines()
#print("Comments => \n\n", all_comments, "\n")

# Set a list of stop words. Used to filter the comments. Can add more of common words.
stop_words = set(stopwords.words("english"))
#print("Stop words => \n\n", stop_words, "\n")

comments_tokenized = filter_tokenize(all_comments)

most_common = get_common_words(comments_tokenized, 100)
print("Most common words = \n", most_common, "\n")

'''include = ["camera"]
exclude = []
test = find_comments(include, exclude, all_comments)
most_common = get_common_words(filter_tokenize(test), 10)
print("Most common words = \n", most_common, "\n")
#print_list(test)'''

cv=CountVectorizer(max_df=0.85, stop_words=stop_words)
word_count_vector = cv.fit_transform(all_comments)
#print(word_count_vector)
#print(list(cv.vocabulary_.keys())[:10])
tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)

#http://brandonrose.org/clustering
#print_list(all_comments)
#print_list(usefull_comments)
#print(usefull_comments)
#print("Number of all comments=", len(all_comments))
#print("Number of selected comments=", len(usefull_comments))
