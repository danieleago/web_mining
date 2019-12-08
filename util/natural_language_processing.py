import gensim
import spacy

from collections import Counter

from gensim import corpora
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess

from spacy.lang.it.stop_words import STOP_WORDS as STOP_WORDS_IT
from spacy.lang.en.stop_words import STOP_WORDS as STOP_WORDS_EN
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from log.myLogging import myLogger

nlp_it = spacy.load('it')
nlp_en = spacy.load('en_core_web_sm')


def bag_of_words(words):
    words_dictionary = Counter()
    for word in words:
        words_dictionary[word] +=1
    return words_dictionary


def find_entity(text, lang):
    if lang == 'it':
        doc = nlp_it(text)
    elif lang == 'en':
        doc = nlp_en(text)
    else:
        return None
    return doc.ents


def lemmatization(words,lang='it', allowed_postags=['ADJ', 'ADV', 'NOUN']):
    """https://spacy.io/api/annotation"""
    if lang =='it':
        nlp_ = nlp_it
    elif lang =='en':
        nlp_ = nlp_en
    doc = nlp_(" ".join(words))
    return [token.lemma_ for token in doc if token.pos_ in allowed_postags]


def lemmatization_with_verb(words, lang='it', allowed_postags=['ADJ', 'ADV', 'NOUN', 'VERB']):
    """https://spacy.io/api/annotation"""
    if lang =='it':
        nlp_ = nlp_it
    elif lang =='en':
        nlp_ = nlp_en
    doc = nlp_(" ".join(words))
    return [token.lemma_ for token in doc if token.pos_ in allowed_postags]


def remove_stopwords(text,lang = 'it'):
    if lang == 'it':
        stop_words = STOP_WORDS_IT
    elif lang == 'en':
        stop_words = STOP_WORDS_EN

    preprocessed = simple_preprocess(text)
    return [word for word in preprocessed if word not in stop_words]


def show_wordcloud(data, title="cloud", lang='it'):

    if lang == 'it':
        stop_words = STOP_WORDS_IT
    elif lang == 'en':
        stop_words = STOP_WORDS_EN

    wordcloud = WordCloud(
        background_color='white',
        stopwords=stop_words,
        max_words=200,
        max_font_size=40,
        scale=3,
        random_state=1  # chosen at random by flipping a coin; it was heads
    ).generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    if title:
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()


def tokenize_and_lemmarization(text,lang = 'it'):
    words = remove_stopwords(text,lang)
    return lemmatization(words,lang)


def tokenize_and_lemmarization_with_verb(text):
    words = remove_stopwords(text)
    return lemmatization_with_verb(words)


def topic_clustering(texts):

    # Corpus
    print(len(texts))

    # Dictionary
    id2word = corpora.Dictionary(texts)

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    coherence_values = []

    show_wordcloud(' '.join(str(r) for v in texts for r in v))

    def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=2):
        """
            Compute c_v coherence for various number of topics

            Parameters:
            ----------
            dictionary : Gensim dictionary
            corpus : Gensim corpus
            texts : List of input texts
            limit : Max num of topics

            Returns:
            -------
            model_list : List of LDA topic models
            coherence_values : Coherence values corresponding to the LDA model with respective number of topics
            """
        top_number_topics = 1
        previous_coherence = 0
        previous_model = None

        for num_topics in range(start, limit, step):
            model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                    id2word=id2word,
                                                    num_topics=num_topics,
                                                    random_state=100,
                                                    update_every=1,
                                                    chunksize=100,
                                                    passes=10,
                                                    alpha='auto',
                                                    per_word_topics=True)

            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')

            coherence_values.extend([coherencemodel.get_coherence()])
            diff = coherencemodel.get_coherence() - previous_coherence
            print(diff)
            if diff < 0.01:
                return previous_model, top_number_topics, previous_coherence

            else:
                top_number_topics = num_topics
                previous_coherence = coherencemodel.get_coherence()
                previous_model = model

    # Can take a long time to run.
    optimal_model, top_number_topics, coherence = compute_coherence_values(dictionary=id2word, corpus=corpus,
                                                                            texts=texts,
                                                                           start=2, limit=10, step=2)

    print(optimal_model.print_topics())

    # Print the Keyword in the 10 topics
    myLogger.info("Coherence ", coherence)



