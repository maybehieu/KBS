import math
import string
from underthesea import word_tokenize
from controller.utils import tokenizer
import pandas as pd


def preprocess(text):
    # Convert to lowercase and remove punctuation
    text = text.lower()
    return tokenizer(text)
    # return text.split(" ")


def create_word_dict(total, sentence):
    wordDict = dict.fromkeys(total, 0)
    for word in sentence:
        try:
            wordDict[word] += 1
        except:
            pass
    return wordDict


def compute_tf(wordDict, doc):
    tfDict = {}
    corpusCount = len(doc)
    for word, count in wordDict.items():
        tfDict[word] = count / float(corpusCount)
    return tfDict


# def compute_idf(docList):
#     idfDict = {}
#     N = len(docList)

#     idfDict = dict.fromkeys(docList[0].keys(), 0)
#     for word, val in idfDict.items():
#         idfDict[word] = math.log10(N / (float(val) + 1))

#     return idfDict


def compute_idf(docList=[]):
    idfDict = {}
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for word, val in idfDict.items():
        count = 0
        for _dict in docList:
            try:
                if _dict[word] > 0:
                    count += 1
            except:
                pass
        if count == 0:
            count = 1
        idfDict[word] = math.log(N / float(count))

    return idfDict


def compute_tfidf(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val * idfs[word]
    return tfidf


def compute_tf_df(wordDict, doc):
    tf_df = {}
    docCount = len(doc)

    # Calculate Term Frequency (TF)
    for word, count in wordDict.items():
        tf = count / float(docCount)

        # Calculate Document Frequency (DF)
        df = sum(1 for d in doc if word in d)

        # Calculate TF-DF
        tf_df[word] = tf * df

    return tf_df


def cosine_similarity(tfidf_vector1, tfidf_vector2):
    # Calculate the dot product of the two vectors
    dot_product = sum(
        tfidf_vector1[term] * tfidf_vector2[term]
        for term in tfidf_vector1
        if term in tfidf_vector2
    )

    # Calculate the magnitude (Euclidean norm) of each vector
    magnitude1 = math.sqrt(sum(tfidf_vector1[term] ** 2 for term in tfidf_vector1))
    magnitude2 = math.sqrt(sum(tfidf_vector2[term] ** 2 for term in tfidf_vector2))

    # Calculate the cosine similarity
    if magnitude1 == 0 or magnitude2 == 0:
        return 0  # Avoid division by zero
    else:
        return dot_product / (magnitude1 * magnitude2)


def process_tfidf(lst, query):
    _lst = [preprocess(sent) for sent in lst]
    _query = preprocess(query)

    total = [word for sent in _lst for word in sent]
    total.extend(_query)

    total = list(set(total))
    wordDicts = [create_word_dict(total, sentence) for sentence in _lst]
    q_wordDict = create_word_dict(total, _query)

    tfList = []
    for idx in range(len(lst)):
        tfList.append(compute_tf(wordDicts[idx], _lst[idx]))
    tfQuery = compute_tf(q_wordDict, _query)
    idfs = compute_idf(wordDicts + [q_wordDict])

    tfidfList = []
    for idx in range(len(lst)):
        tfidfList.append(compute_tfidf(tfList[idx], idfs))
    q_tfidf = compute_tfidf(tfQuery, idfs)

    frame = pd.DataFrame(tfidfList + [q_tfidf])

    sims = [cosine_similarity(q_tfidf, s) for s in tfidfList]


    return zip(lst, sims)


def find_cate(z, *cates):
    sort = sorted(z, key=lambda x: x[1], reverse=True)
    s, sims = zip(*sort)

    for string, sim in zip(s, sims):
        print(f'độ tương đồng giữa "{string}" và "{query}" là {sim:.4f}')
    
    top = s[:5]
    max_match_count = 0
    list_with_most_matches = None
    for lst in cates:
        match_count = len(set(top) & set(lst))
        if match_count > max_match_count:
            max_match_count = match_count
            list_with_most_matches = lst

    print(list_with_most_matches)


def process_tfidf_joined(lst, query):
    _lst = [preprocess(sent) for sent in lst]
    _query = preprocess(query)

    total = [word for sent in _lst for word in sent]
    total.extend(_query)

    total = list(set(total))

    joined = ""
    for sent in lst:
        joined += sent + " "
    joined += query
    # print(joined)
    _joined = preprocess(joined)
    print(_joined)
    worddict = create_word_dict(total, _joined)
    q_wordDict = create_word_dict(total, _query)

    tf = compute_tf(worddict, _joined)
    tfQuery = compute_tf(q_wordDict, _query)

    idfs = compute_idf([tf, tfQuery])

    tfidf = compute_tfidf(tf, idfs)
    q_tfidf = compute_tfidf(tfQuery, idfs)

    frame = pd.DataFrame([tfidf, q_tfidf])

    print(frame)

    sims = cosine_similarity(q_tfidf, tfidf)

    # for string, sim in zip(lst, sims):
    #     print(f'độ tương đồng giữa "{string}" và "{query}" là {sim:.4f}')
    print(f"độ tương đồng tương đối: {sims}")


def process_tfdf(lst, query):
    _lst = [preprocess(sent) for sent in lst]
    _query = preprocess(query)

    total = [word for sent in _lst for word in sent]
    total.extend(_query)

    total = list(set(total))
    wordDicts = [create_word_dict(total, sentence) for sentence in _lst]
    q_wordDict = create_word_dict(total, _query)

    # tfList = []
    # for idx in range(len(lst)):
    #     tfList.append(compute_tf(wordDicts[idx], _lst[idx]))
    # tfQuery = compute_tf(q_wordDict, _query)
    # # idfs = compute_idf(tfList + [tfQuery])

    tfdfList = []
    for idx in range(len(lst)):
        tfdfList.append(compute_tf_df(wordDicts[idx], _lst[idx]))
    q_tfdf = compute_tf_df(q_wordDict, _query)

    frame = pd.DataFrame(tfdfList + [q_tfdf])

    print(frame)

    sims = [cosine_similarity(q_tfdf, s) for s in tfdfList]

    for string, sim in zip(lst, sims):
        print(f'độ tương đồng giữa "{string}" và "{query}" là {sim:.4f}')


def levenshtein_distance(str1, str2):
    m, n = len(str1), len(str2)

    # Create a matrix to store the costs
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the first row and first column
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill in the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)

    # The final cell contains the Levenshtein Distance
    return dp[m][n]


def process_lavenshtein(lst, query):
    for sent in lst:
        print(
            f'khoảng cách lavenshtein giữa "{sent}" và "{query}" là {levenshtein_distance(sent, query)}'
        )


def jaccard_similarity(str1, str2):
    # Tokenize the input strings into sets of words
    set1 = set(str1.split())
    set2 = set(str2.split())

    # Calculate the Jaccard Similarity
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection

    if union == 0:
        return 0.0  # Avoid division by zero for empty sets
    else:
        return float(intersection) / union


def process_jaccard(lst, query):
    for sent in lst:
        print(
            f'độ tương đồng jaccard giữa "{sent}" và "{query}" là {jaccard_similarity(sent, query)}'
        )


# Example usage
sentences = [
    "thay đổi thời tiết",
    "thời tiết thất thường",
    "thời tiết không đẹp",
    "chuyển mùa",
    "giao mùa",
    "thời tiết bất lợi",
]
s2 = [
    "nhiệt độ thời tiết",
    "nhiệt độ thất thường",
    "nhiệt độ không đẹp",
    "chuyển mùa",
    "giao mùa",
    "nhiệt độ bất lợi",
]
s3 = [
    "thay đổi độ ẩm",
    "độ ẩm thất thường",
    "độ ẩm không đẹp",
    "mưa",
    "nắng gắt",
    "độ ẩm bất lợi",
]
query = "giao mùa"

# process_tfidf_joined(sentences, query)
# process_tfidf_joined(s2, query)
# process_tfidf_joined(s3, query)

z = process_tfidf(sentences + s2 + s3, query)
print(find_cate(z, sentences, s2, s3))
# process_tfidf(s2, query)
# process_tfidf(s3, query)

# process_lavenshtein(sentences, query)
# process_jaccard(sentences, query)
# process_jaccard(s2, query)
# process_jaccard(s3, query)

# process_tfdf(sentences, query)
# process_tfdf(s2, query)
# process_tfdf(s3, query)
