import json
import math
import pickle
import csv

from utils import normalize, tokenize, Posting, PostingsList, process_verbs
from parsivar import FindStems


def save_most_frequent_terms(index):
    with open('data/frequents.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        field = ["term", "frequency"]
        writer.writerow(field)
        for term, postings_list in index.items():
            writer.writerow([term, postings_list.frequency])


def tf_idf(term, posting):
    term_freq = posting.frequency
    document_freq = len(final_positional_index[term].postings.keys())
    total_docs = len(contents)
    return (1 + math.log10(term_freq)) * math.log10(total_docs / document_freq)
    # return (1 + math.log10(term_freq))
    # return (1 + (term_freq)) * math.log10(total_docs / document_freq)


if __name__ == '__main__':
    with open('data/IR_data_news_12k.json', 'r', encoding='utf-8') as json_file:
        raw_data = json.loads(json_file.read())

    new_content = "به گزارش روابط عمومی دانشگاه صنعتی امیرکبیر: در بیست و چهارمین دوره از مسابقات بین‌المللی برنامه‌نویسی دانشجویی ICPC در منطقه‌ی غرب آسیا که با حضور ۸۰ تیم از دانشگاه‌های مختلف کشور در دانشگاه صنعتی شریف برگزار شد؛ تیم برنامه نویسی دانشکده مهندسی کامپیوتر دانشگاه صنعتی امیرکبیر موفق به کسب مقام سوم دانشگاهی و مقام دوم تیمی و مدال نقره در این دوره از مسابقات شد."
    new_title = "دانشجویان دانشکده مهندسی کامپیوتر دانشگاه صنعتی امیرکبیر در مسابقات بین المللی برنامه سازی دانشجویی منطقه ای غرب آسیا به مقام سوم دست یافتند. "
    new_url = "urllllllll"


    contents = {}
    titles = {}
    urls = {}

    for index, data in raw_data.items():
        contents[index] = data['content']
        titles[index] = data['title']
        urls[index] = data['url']

    index = '12202'
    contents[index] = new_content
    titles[index] = new_title
    urls[index] = new_url

    contents = {key: normalize(value) for key, value in contents.items()}  # normalizing

    stemmer = FindStems()
    positional_inverted_index = {}
    for index, data in contents.items():
        tokens = tokenize(data)  # tokenizing
        tokens = process_verbs(tokens)
        for position, token in enumerate(tokens):
            token = stemmer.convert_to_stem(token)  # stemming
            if token in positional_inverted_index.keys():
                positional_inverted_index[token].frequency += 1
                if token not in positional_inverted_index[token].postings.keys():
                    posting = Posting()
                    positional_inverted_index[token].postings[index] = posting

                positional_inverted_index[token].postings[index].frequency += 1
                positional_inverted_index[token].postings[index].positions.append(position)
            else:
                postings_list = PostingsList()
                positional_inverted_index[token] = postings_list
                positional_inverted_index[token].frequency += 1
                posting = Posting()
                posting.frequency += 1
                posting.positions.append(position)
                positional_inverted_index[token].postings[index] = posting

    sorted_positional_index_by_frequency = dict(sorted(positional_inverted_index.items(), key=lambda x:x[1].frequency, reverse=True))  # sort by frequency
    save_most_frequent_terms(dict(list(sorted_positional_index_by_frequency.items())[:50]))
    final_positional_index = dict(list(sorted_positional_index_by_frequency.items())[50:])  # eliminate top 50 most frequent terms

    new_doc_vector = {}
    doc_vector_length = {}
    for term, postings_list in final_positional_index.items():
        postings = postings_list.postings
        for doc_id, posting in postings.items():
            weight = tf_idf(term, posting)
            posting.tf_idf += weight
            if doc_id in doc_vector_length.keys():
                doc_vector_length[doc_id] += weight ** 2
            else:
                doc_vector_length[doc_id] = weight ** 2
            if doc_id == '12202':
                print(f"term: {term}, weight before normalizing: {weight}")
                new_doc_vector[term] = weight

    print("---------------------------------------------------------------")

    new_doc_length = math.sqrt(doc_vector_length['12202'])
    for term, weight in new_doc_vector.items():
        print(f"term: {term}, weight after normalizing: {weight/new_doc_length}")
        new_doc_vector[term] = weight/new_doc_length


    print('-------------------------------------------------------------')

    print(new_doc_vector)


    for doc_id, length in doc_vector_length.items():
        normalized_length = math.sqrt(length) if length > 0 else 1
        for postings_list in final_positional_index.values():
            if doc_id in postings_list.postings.keys():
                postings_list.postings[doc_id].tf_idf /= normalized_length

    champions_list = {}
    for term, postings_list in final_positional_index.items():
        postings = postings_list.postings
        postings_sorted_by_weight = dict(sorted(postings.items(), key=lambda item: item[1].tf_idf, reverse=True))
        champions_list[term] = PostingsList()
        champions_list[term].postings = dict(list(postings_sorted_by_weight.items())[:100])
        champions_list[term].frequency = postings_list.frequency

    print(f'size of dictionary: {len(final_positional_index.keys())}')

    with open('data/positional_inverted_index.pickle', 'wb') as indox_file:
        pickle.dump(final_positional_index, indox_file)

    with open('data/champions_list.pickle', 'wb') as champions_file:
        pickle.dump(champions_list, champions_file)

