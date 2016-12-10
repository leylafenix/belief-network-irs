from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import swadesh
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import nltk
import os


# Procesa un fichero txt/pdf
def process(path, query, language=None):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.pdf'):
                os.system("pdftotext " + str(os.path.join(root, file) + " " + str(os.path.join(root, file)[:-4]) + ".txt"))

    corpus = PlaintextCorpusReader(path, '.*\.txt')

    if not language:
        language = identify_language(corpus)

    if not language:
        return None, 'No fue posible detectar el idioma del corpus'

    print(language)

    stopwordlist = stopwords.words(language)

    documents = {}

    for c in corpus.fileids():
        stemmer = nltk.SnowballStemmer(language)
        documents[c] = [stemmer.stem(w) for w in corpus.words(c) if w not in stopwordlist]

    query = [stemmer.stem(q) for q in query if q not in stopwordlist]
    query = process_query(query)

    # Retorna un diccionario {nombre del documento: lista de términos en el documento}
    # y una lista con los términos de la query procesada
    return documents, query


language_dic = {'english': 'en', 'spanish': 'es', 'german': 'de', 'french': 'fr', 'italian': 'it', 'portuguese': 'pt'}


def identify_language(corpus):
    s_ratio = stopwords_ratio(corpus)
    c_ratio = common_words_ratio(corpus)

    return max([(s_ratio[l] + c_ratio[l], l) for l in language_dic])[1]


def stopwords_ratio(corpus):
    ratio = {}

    for language in language_dic:
        ratio[language] = 0
        for c in corpus.fileids():
            stopwords_set = set(stopwords.words(language))
            word_set = set(corpus.words(c))
            ratio[language] += len(stopwords_set.intersection(word_set))

    return ratio


def common_words_ratio(corpus):
    ratio = {}

    for language, value in language_dic.items():
        ratio[language] = 0
        for c in corpus.fileids():
            swadesh_set = set(swadesh.words(value))
            word_set = set(corpus.words(c))
            ratio[language] += len(swadesh_set.intersection(word_set))

    return ratio


def process_query(query):
    result = list(query)

    for q in query:
        ss = wordnet.synsets(q)
        if len(ss) == 1:
            result += [l.name() for l in ss[0].lemmas()]

    return list(set(result))


def unusual_words(text):
    text_vocab = set(w.lower() for w in text if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    unusual = text_vocab.difference(english_vocab)
    return sorted(unusual)