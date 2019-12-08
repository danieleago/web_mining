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

    def compute_coherence_values(dictionary, corpus, texts):
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

        model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=5,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)

        # Calcola la coerenza tra i topic
        #coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')

        """Get the most significant topics (alias for `show_topics()` method).

                Parameters
                ----------
                num_topics : int, optional
                    The number of topics to be selected, if -1 - all topics will be in result (ordered by significance).
                num_words : int, optional
                    The number of words to be included per topics (ordered by significance).

                Returns
                -------
                list of (int, list of (str, float))
                    Sequence with (topic_id, [(word, value), ... ])."""

        myLogger.info("topics :" + str(model.print_topics()))

    compute_coherence_values(id2word, corpus, texts)



