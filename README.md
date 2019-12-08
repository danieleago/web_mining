# WebMining

## Prerequisites
This package assumes using Python 3.x. 

Expected package dependencies are listed in the "requirements.txt" file for PIP, you need to run the following commands to get dependencies:
```
pip install -r requirements.txt

python -m spacy download en_core_web_sm
python -m spacy download it_core_news_sm
```

## Details
Use the script keywordExtraction.py to get the keywords and entities related to web page. It also generates a word cloud.

Use the script crawlerDomain.py to crawl a list of urls. The script extracts keywords from web pages found and estimates the topics contained in the pages.
