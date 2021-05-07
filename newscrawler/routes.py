import io
import string
from flask import render_template, send_file
from newscrawler import app
from newscrawler.models import Agency, Article
from datetime import date
from wordcloud import WordCloud, STOPWORDS
from PIL import Image


def average(agency, sent, neut):
    if not hasattr(agency, 'count'):
        agency.count = 1
        agency.sent = 0
        agency.neut = 0
    agency.sent += (sent - agency.sent) / agency.count
    agency.neut += (neut - agency.neut) / agency.count


@app.route('/')
def index():
    articles = Article.query.filter(Article.date==date.today()).all()
    structure = {}
    for article in articles:
        average(article.agency, article.sentiment, article.neutrality)
        if article.agency in structure:
            structure[article.agency].append(article)
        else:
            structure[article.agency] = [article]
    for agency in structure.keys():
        agency.sent = round(agency.sent, 2)
        agency.neut = round(agency.neut, 2)
        structure[agency].sort(key=lambda l: l.sentiment, reverse=True)
    return render_template('index.html',
                           count=len(articles),
                           structure=structure)


@app.route('/agencies')
def agencies():
    agencies = Agency.query.all()
    return render_template('agencies.html', agencies=agencies)


@app.route('/agency/<agency>')
def agency(agency):
    agency = Agency.query.filter(Agency.name == agency).first_or_404()
    return render_template('agency.html', agency=agency, Article=Article)


stopwords = list(STOPWORDS)
stopwords.extend(['say', 'said', 'news', 'app', 'says'])
stopwords.extend([l for l in string.ascii_lowercase + string.ascii_uppercase])
@app.route('/agency/<agency>/wordcloud')
def agencywordcloud(agency):
    agency = Agency.query.filter(Agency.name == agency).first_or_404()
    text = []
    for article in agency.articles.filter(Article.date==date.today()):
        text.append(article.text)

    wordcloud = WordCloud(
        width=600, height=400, background_color='white',
        stopwords=stopwords)\
        .generate(' '.join(text)).to_array()

    img = Image.fromarray(wordcloud.astype('uint8'))
    file_object = io.BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/png')
