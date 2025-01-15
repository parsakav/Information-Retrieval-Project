import os
import string

print(string.punctuation)

def remove_punctuations(text :str)->str:

    s = [x for x in text if x not in string.punctuation]
    return ''.join(s)

def read_documents(baseUrl: str):
    for path in os.listdir('Documents'):
        with open(f'Documents/{path}', "+r") as file:
            print(remove_punctuations(file.read().lower()))


read_documents(baseUrl='Document')
