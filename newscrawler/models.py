from newscrawler import db
from sqlalchemy.ext.declarative import declared_attr

class Base(db.Model):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)


class Article(Base):
    __tablename__ = 'article'

    url = db.Column(db.String)
    title = db.Column(db.String)
    date = db.Column(db.Date)
    byline = db.Column(db.String)
    text = db.Column(db.Text)
    pos = db.Column(db.Float)
    neu = db.Column(db.Float)
    neg = db.Column(db.Float)
    compound = db.Column(db.Float)

    agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))

    def __repr__(self):
        return f'<Article {self.agency.name}: {self.title} {self.date}>'


class Agency(Base):
    __tablename__ = 'agency'

    name = db.Column(db.String)
    homepage = db.Column(db.String)
    articles = db.relationship('Article', backref='agency')

    def __repr__(self):
        return f'<Agency {self.name}: {self.homepage} ({len(self.articles)}) articles>'
