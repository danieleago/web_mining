import re

from newspaper import Article
from util.natural_language_processing import bag_of_words, tokenize_and_lemmarization, show_wordcloud, find_entity
from log.myLogging import myLogger


def readArticle(link, lang='it', generate_cloud=False):

    try:
        a = Article(link, language=lang)

        a.download()
        a.parse()

        a.nlp()

        text = a.text

        tokens = tokenize_and_lemmarization(text, lang)

        if generate_cloud:
            show_wordcloud(' '.join(tokens))

        tags = bag_of_words(tokens)

        keywords = tags.most_common(15)

        keywords = [keyword[0] for keyword in keywords]

        entities = find_entity(text, lang)

        myLogger.info(link + ": " + "keywords: " + ", ".join(keywords) + ", entities: " + ", ".join(re.sub('[^A-Za-z0-9 ]+', '', ent.text) for ent in entities))

        return keywords

    except:
        myLogger.info(link + " error scraping")
