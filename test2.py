import math
import string
from underthesea import word_tokenize
from controller.utils import tokenizer

# call first
def preprocess(text):
    # Convert to lowercase and remove punctuation
    text = text.lower()
    return tokenizer(text)

def build_vocabulary(sentences=[['']]):
    vocabulary = set()
    for sentence in sentences:
        for word in sentence:
            vocabulary.update(word)
    return list(vocabulary)

def calculate_tfidf_values(sentences=[['']], vocabulary=[]):
    tfidf_values = []
    for sentence in sentences:
        tfidf_vector = []
        for word in vocabulary:
            # Calculate TF
            tf = sentence.count(word)
            # Calculate IDF
            idf = calculate_idf(word)
            # Calculate TF-IDF
            tfidf = tf * idf
            tfidf_vector.append(tfidf)
        tfidf_values.append(tfidf_vector)
    return tfidf_values

def calculate_idf(word, sentences):
    num_docs_with_word = sum(1 for doc in sentences if word in doc)
    return math.log(len(sentences) / (1 + num_docs_with_word))

def calculate_cosine_similarity(query):
    query = preprocess(query)
    query_vector = calculate_tfidf_vector(query)
    similarities = []
    for sentence_vector in tfidf_values:
        similarity = calculate_cosine_similarity_between_vectors(query_vector, sentence_vector)
        similarities.append(similarity)
    return similarities



def calculate_tfidf_vector(text):
    tfidf_vector = []
    for word in vocabulary:
        tf = text.split().count(word)
        idf = calculate_idf(word)
        tfidf = tf * idf
        tfidf_vector.append(tfidf)
    return tfidf_vector

def calculate_cosine_similarity_between_vectors(vector1, vector2):
    dot_product = sum(x * y for x, y in zip(vector1, vector2))
    magnitude_vector1 = math.sqrt(sum(x ** 2 for x in vector1))
    magnitude_vector2 = math.sqrt(sum(x ** 2 for x in vector2))
    similarity = dot_product / (magnitude_vector1 * magnitude_vector2)
    return similarity