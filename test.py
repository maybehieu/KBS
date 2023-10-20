import math
import string
from underthesea import word_tokenize
from controller.utils import tokenizer

def preprocess(text):
    # Convert to lowercase and remove punctuation
    text = text.lower()
    return tokenizer(text)

def calculate_tf(text):
    # Calculate Term Frequency for each word in the text
    words = text.split()
    tf = {}
    for word in words:
        tf[word] = tf.get(word, 0) + 1
    return tf

def calculate_idf(corpus, word):
    # Calculate Inverse Document Frequency for a word in the corpus
    num_docs_with_word = sum(1 for doc in corpus if word in doc)
    return math.log(len(corpus) / (1 + num_docs_with_word))

def calculate_tfidf(query, sentences):
    # Preprocess query and sentences
    query = preprocess(query)
    sentences = [preprocess(sentence) for sentence in sentences]

    # Build the vocabulary
    vocabulary = set(word for sentence in sentences for word in sentence)

    # Calculate TF-IDF values
    tfidf_values = []

    for sentence in sentences:
        tfidf_vector = []
        for word in vocabulary:
            # Calculate TF
            tf = sentence.count(word)
            # Calculate IDF
            idf = calculate_idf(sentences, word)
            # Calculate TF-IDF
            tfidf = tf * idf
            tfidf_vector.append(tfidf)
        tfidf_values.append(tfidf_vector)


    # Calculate TF-IDF vector for the query
    query_vector = []
    for word in vocabulary:
        tf = query.count(word)
        idf = calculate_idf(sentences, word)
        tfidf = tf * idf
        query_vector.append(tfidf)

    return query_vector, tfidf_values

def calculate_cosine_similarity(query_vector, sentence_vector):
    dot_product = sum(x * y for x, y in zip(query_vector, sentence_vector))
    magnitude_query = math.sqrt(sum(x ** 2 for x in query_vector))
    magnitude_sentence = math.sqrt(sum(x ** 2 for x in sentence_vector))
    similarity = dot_product / (magnitude_query * magnitude_sentence)
    return similarity

# Example usage
sentences = ["thay đổi thời tiết", "thời tiết thất thường", "thời tiết không đẹp"]
query = "thời tiết thay đổi"

query_vector, tfidf_values = calculate_tfidf(query, sentences)

similarities = []
for sentence_vector in tfidf_values:
    similarity = calculate_cosine_similarity(query_vector, sentence_vector)
    similarities.append(similarity)

for i, sim in enumerate(similarities):
    print(f"Similarity between query and sentence {i+1}: {sim}")