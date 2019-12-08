from newspaper import Article
from util.natural_language_processing import bag_of_words, tokenize_and_lemmarization, show_wordcloud
from log.myLogging import myLogger


def readArticle(link, lang='it', generate_cloud=False):

    try:
        a = Article(link, language=lang)

        a.download()
        a.parse()

        a.nlp()

        result = a.text

        tokens = tokenize_and_lemmarization(result, lang)

        if generate_cloud:
            show_wordcloud(' '.join(tokens))

        tags = bag_of_words(tokens)

        keywords = tags.most_common(15)

        keywords = [keyword[0] for keyword in keywords]

        myLogger.info(link + ": " + " ".join(keywords))

        return keywords

    except:
        myLogger.info(link + " error scraping")
