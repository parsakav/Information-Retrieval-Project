import os
import re
import string
from collections import defaultdict
from math import log

print(string.punctuation)


#remove punctuations (e.g . @ ,)
def remove_punctuations(text: str) -> str:
    s = [x for x in text if x not in string.punctuation]
    return ''.join(s)


#read document
def read_document(document: str) -> str:
    with open(f'Documents/{document}', "r") as file:
        #lower str helps us to implement case insenstive query
        return remove_punctuations(file.read().lower())


#read all documents in Documents folder
def read_documents() -> dict:
    d = dict()
    for path in os.listdir('Documents'):
        d[path] = read_document(path)
    return d;


#create inverted index . the key is term and the value is lists of doc id's
def inverted_index() -> dict:
    docs = read_documents()
    invertedindex = dict()
    for x in docs:
        l = docs[x].split()
        for z in l:
            if z in invertedindex:
                invertedindex[z].add(x)
            else:
                invertedindex[z] = {x}

    return invertedindex


#  Boolean Query Processing
def boolean_query(inverted_index, query):
    query = query.lower()
    print("query:", query)
    terms = query.split()
    print("terms:", terms)
    result = set()

    if 'and' in terms:
        terms.remove('and')
        term1, term2 = terms
        result = set(inverted_index.get(term1, [])) & set(inverted_index.get(term2, []))
    elif 'or' in terms:
        terms.remove('or')
        term1, term2 = terms
        result = set(inverted_index.get(term1, [])) | set(inverted_index.get(term2, []))
    elif 'not' in terms:
        terms.remove('not')
        term1, term2 = terms
        result = set(inverted_index.get(term1, [])) - set(inverted_index.get(term2, []))
    else:
        result = set(inverted_index.get(terms[0], []))

    return list(result)


# Wildcard Search
def wildcard_search(inverted_index, wildcard):
    regex = re.compile(wildcard.replace('*', '.*').replace('?', '.?'))
    matching_terms = [term for term in inverted_index if regex.fullmatch(term)]
    result = set()
    for term in matching_terms:
        result.update(inverted_index[term])
    return list(result)


def create_tfidf_index() -> dict:
    docs = read_documents()
    term_freqs = defaultdict(dict)  # term -> {doc: count}
    doc_lengths = defaultdict(int)  # doc -> total words in doc

    # Calculate term frequencies and document lengths
    for doc, content in docs.items():
        words = content.split()
        doc_lengths[doc] = len(words)
        for word in words:
            term_freqs[word][doc] = term_freqs[word].get(doc, 0) + 1

    # Calculate IDF values
    total_docs = len(docs)
    idf = {term: log(total_docs / len(doc_freqs)) for term, doc_freqs in term_freqs.items()}

    # Create TF-IDF index
    tfidf_index = defaultdict(dict)
    for term, doc_freqs in term_freqs.items():
        for doc, freq in doc_freqs.items():
            tfidf = (freq / doc_lengths[doc]) * idf[term]  # TF-IDF formula
            tfidf_index[term][doc] = tfidf

    return tfidf_index


#implement multi operator boolean query
def advanced_boolean_query(inverted_index, query):
    print(f"query:{query}")
    q = query.split()
    results = set(boolean_query(inverted_index, f'{q[0]} {q[1]} {q[2]}'))
    x = 3
    while x < len(q):
        if q[x] == 'and':
            results = results & set(inverted_index.get(q[x], []))
        elif q[x] == 'or':
            results = results | set(inverted_index.get(q[x], []))
        elif q[x] == 'not':
            results = results - set(inverted_index.get(q[x], []))
        x += 2
    return results


#print(inverted_index())

print("************************  Boolean Query Processing  ***********************************")
print(boolean_query(inverted_index(), "swaying or pop"))
print(boolean_query(inverted_index(), "swaying and pop"))
print(boolean_query(inverted_index(), "swaying not pop"))
print(boolean_query(inverted_index(), "weather or pop"))
print(advanced_boolean_query(inverted_index(), "weather or pop or the"))
print("************************  Wild Card  ***********************************")

print(wildcard_search(inverted_index(), "*ing"))
print(wildcard_search(inverted_index(), "shop*"))
print(wildcard_search(inverted_index(), "*ppi*"))
print(wildcard_search(inverted_index(), "sho*ng"))
print(wildcard_search(inverted_index(), "mY*"))
print(wildcard_search(inverted_index(), "g?t"))

print("************************  tfidf  ***********************************")

#print(create_tfidf_index())
print("************************  Boolean Query Processing  ***********************************")
print(boolean_query(create_tfidf_index(), "swaying or pop"))
print("************************  Wild Card  ***********************************")

print(wildcard_search(create_tfidf_index(), "*ing"))
print(wildcard_search(create_tfidf_index(), "shop*"))
print(wildcard_search(create_tfidf_index(), "*ppi*"))
print(wildcard_search(create_tfidf_index(), "sho*ng"))
print(wildcard_search(create_tfidf_index(), "mY*"))
print(wildcard_search(create_tfidf_index(), "g?t"))


