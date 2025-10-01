import math
import pickle
import time
import json

from parsivar import FindStems
from utils import tokenize, normalize, process_verbs


def get_query_tokens(query):
    normalized_query = normalize(query)
    query_tokens = tokenize(normalized_query)
    query_tokens = process_verbs(query_tokens)
    stemmer = FindStems()
    stemmed_tokens = [stemmer.convert_to_stem(token) for token in query_tokens]
    return stemmed_tokens


def calculate_scores(index, query_tokens):
    doc_scores = {}
    for query_token in query_tokens:
        postings_list = index[query_token]
        for doc_id, posting in postings_list.postings.items():
            if doc_id in doc_scores:
                doc_scores[doc_id] += posting.tf_idf #* query_tokens.count(query_token)
            else:
                doc_scores[doc_id] = posting.tf_idf #* query_tokens.count(query_token)
    return doc_scores


def calculate_cosine_score(index, query_tokens):
    doc_scores = {}
    query_tf_idf = {}
    query_tf = {}
    query_length = 0

    for token in query_tokens:
        if token in query_tf:
            query_tf[token] += 1
        else:
            query_tf[token] = 1

    # unique_tokens = set(query_tokens)
    for query_token, tf in query_tf.items(): #  query_tf.items
        if query_token in index:
            idf = math.log10(len(contents) / len(index[query_token].postings))
            query_tf_idf[query_token] = idf * (1 + math.log10(tf))
            query_length += idf ** 2

    query_length = math.sqrt(query_length)
    for query_token, tf_idf in query_tf_idf.items():
        query_tf_idf[query_token] = tf_idf / query_length

    for query_token, tf_idf in query_tf_idf.items():
        for doc_id, posting in index[query_token].postings.items():
            doc_tf_idf = posting.tf_idf
            if doc_id in doc_scores:
                doc_scores[doc_id] += tf_idf * doc_tf_idf
            else:
                doc_scores[doc_id] = tf_idf * doc_tf_idf

    return doc_scores


def get_top_k(doc_scores, k):
    sorted_scores = dict(sorted(doc_scores.items(), key=lambda x: x[1], reverse=True))
    return dict(list(sorted_scores.items())[:k])


if __name__ == '__main__':
    with open('data/IR_data_news_12k.json', 'r', encoding='utf-8') as json_file:
        raw_data = json.loads(json_file.read())

    contents = {}
    titles = {}
    urls = {}
    for index, data in raw_data.items():
        contents[index] = data['content']
        titles[index] = data['title']
        urls[index] = data['url']

    with open('data/positional_inverted_index.pickle', 'rb') as index_file:
        positional_index = pickle.load(index_file)

    with open('data/champions_list.pickle', 'rb') as champions_file:
        champions_list = pickle.load(champions_file)

    print("doc 47")
    print(contents['47'])


    i = 0
    postings_list = positional_index["دانشگاه"]

    max = 0
    max_doc_id = 0
    min = 1000
    min_doc_id = 0
    zero_printed = False
    for doc_id, posting in postings_list.postings.items():
        if posting.tf_idf > max:
            max_doc_id = doc_id
            max = posting.tf_idf
        if posting.tf_idf < min:
            min = posting.tf_idf
            min_doc_id = doc_id

    print("maximum wight")
    print(f"doc_id: {max_doc_id}")
    print(f"title: {titles[max_doc_id]}")
    print(f"content: {contents[max_doc_id]}")
    print(f"weight: {max}")
    print("--------------------------")


    print("minimum wight")
    print(f"doc_id: {min_doc_id}")
    print(f"title: {titles[min_doc_id]}")
    # print(f"content: {contents[min_doc_id]}")
    print(f"weight: {min}")
    print("--------------------------")



    print("10 first postings of inverted index")
    for doc_id, postings in postings_list.postings.items():
        print(f"doc_id: {doc_id}")
        print(f"title: {titles[doc_id]}")
        print(f"positions: {postings.positions}")
        print("--------------------------")
        i += 1
        if i == 10:
            break

    print("20 first postings of champions list")
    i = 0
    postings_list = champions_list["دانشگاه"]
    for doc_id, postings in postings_list.postings.items():
        print(f"doc_id: {doc_id}")
        print(f"wight: {postings.tf_idf}")
        i += 1
        if i == 20:
            break



    while True:
        query = input('Enter a query: ')
        if query == 'quit':
            break

        try:
            time1 = time.time()
            query_tokens = get_query_tokens(query)
            # doc_scores = calculate_scores(champions_list, query_tokens)
            doc_scores = calculate_cosine_score(champions_list, query_tokens)
            top_k_docs = get_top_k(doc_scores, 10)
            time2 = time.time()
            print(f"time1: {time1}")
            print(f"time2: {time2}")
            print(f"time2 - time1: {time2 - time1}")
            for doc_id in top_k_docs.keys():
                print(f"title: {titles[doc_id]}")
                print(f"content: {contents[doc_id]}")
                print(f"url: {urls[doc_id]}")
                print(f"score: {top_k_docs[doc_id]}")
                print("--------------------------------------")
        except:
            print("no doc to retrieve!")


