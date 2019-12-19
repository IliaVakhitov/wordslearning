from app import db


synonyms = db.Table(
    'synonyms',
    db.Column('word_id', db.Integer, db.ForeignKey('db_words.id')),
    db.Column('synonym_id', db.Integer, db.ForeignKey('db_words.id'))
)


class Word(db.Model):
    __tablename__ = 'db_words'

    id = db.Column(db.Integer, primary_key=True)
    spelling = db.Column(db.String(128))
    definition = db.Column(db.String(550))
    dictionary_id = db.Column(db.Integer, db.ForeignKey('db_dictionaries.id'))
    words_synonyms = db.relationship(
        'Word', secondary=synonyms,
        primaryjoin=(synonyms.c.word_id == id),
        secondaryjoin=(synonyms.c.synonym_id == id),
        backref=db.backref('synonyms', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'<{self.spelling}>'

    def is_synonym(self, word):
        return self.words_synonyms.filter(
            synonyms.c.synonym_id == word.id).count() > 0

    def add_synonym(self, word):
        if not self.is_synonym(word):
            self.words_synonyms.append(word)

    def remove_synonym(self, word):
        if self.is_synonym(word):
            self.words_synonyms.remove(word)


class User(db.Model):
    __tablename__ = 'db_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    secret_question = db.Column(db.String(128))
    secret_answer_hash = db.Column(db.String(128))
    dictionaries = db.relationship('Dictionary', backref='Owner', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Dictionary(db.Model):
    __tablename__ = 'db_dictionaries'

    id = db.Column(db.Integer, primary_key=True)
    dictionary_name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('db_users.id'))
    words = db.relationship('Word', backref='Dictionary',  lazy='dynamic')

    def __repr__(self):
        return f'{self.dictionary_name}'







