import os
import string

print(string.punctuation)


def remove_punctuations(text: str) -> str:
    s = [x for x in text if x not in string.punctuation]
    return ''.join(s)


def read_document(document: str) -> str:
    with open(f'Documents/{document}', "r") as file:
        return remove_punctuations(file.read().lower())


def read_documents() -> dict:
    d = dict()
    for path in os.listdir('Documents'):
        d[path] = read_document(path)
    return d;


def inverted_index() -> dict:
    docs = read_documents()
    print(docs)

    invertedindex = dict()
    for x in docs:
        l = docs[x].split()
        for z in l:
            if z in invertedindex:
                invertedindex[z].add(x)
            else:
                invertedindex[z] = {x}

    return invertedindex


print(inverted_index())
