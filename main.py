import os
import string

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
