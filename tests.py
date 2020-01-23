import json
import unittest

from sqlalchemy import func

from app import create_app, db
from app.models import Word
from appmodel.GameGenerator import GameGenerator
from appmodel.GameType import GameType
from appmodel.RevisionGame import RevisionGame
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class WordModelCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.testing = True
        self.app_client = self.app.test_client()

        db.create_all()
        # Filling db with mock data
        for i in range(50):
            word_i = Word(spelling=f'spelling{i}', definition=f'definition{i}')
            db.session.add(word_i)
        db.session.commit()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_synonym(self):

        # Arrange
        word_house = Word(spelling='house', definition='test word house')
        word_home = Word(spelling='home', definition='test word home')

        # Act
        db.session.add(word_house)
        db.session.add(word_home)
        db.session.commit()

        # Assert
        self.assertEqual(word_house.synonyms.all(), [])
        self.assertEqual(word_home.synonyms.all(), [])

        # Act
        word_house.add_synonym(word_home)
        db.session.commit()

        # Assert
        self.assertTrue(word_house.is_synonym(word_home))
        self.assertEqual(word_house.words_synonyms.count(), 1)
        self.assertEqual(word_house.words_synonyms.first().spelling, 'home')
        self.assertEqual(word_home.synonyms.count(), 1)
        self.assertEqual(word_home.synonyms.first().spelling, 'house')

        # Act
        word_house.remove_synonym(word_home)
        db.session.commit()

        # Assert
        self.assertFalse(word_house.is_synonym(word_home))
        self.assertEqual(word_house.words_synonyms.count(), 0)
        self.assertEqual(word_home.words_synonyms.count(), 0)

    def test_game_generator(self):

        # Arrange
        # data filled in SetUp()

        # Act
        words_limit = 10
        words_list = Word.query.all()
        list1 = GameGenerator.generate_game(words_list, GameType.FindSpelling, words_limit)
        list2 = GameGenerator.generate_game(words_list, GameType.FindSpelling, words_limit)

        # Assert
        self.assertNotEqual(list1, list2, 'Different games cannot be equal')
        # self.assertEqual(len(list1), words_limit, 'Len of game should be equal')
        # self.assertEqual(len(list2), words_limit, 'Len of game should be equal')

    def test_game_data_json(self):
        # Arrange
        # data filled in SetUp()
        word_limit = 5
        game_type = GameType.FindDefinition
        # Act
        words_query = Word.query.order_by(func.random()).limit(word_limit).all()
        revision_game = GameGenerator.generate_game(words_query, game_type, word_limit)
        json_data = json.dumps(revision_game.to_json())
        revision_game1 = RevisionGame(game_type, [])
        revision_game1.load_game_rounds(json.loads(json_data))
        # Assert
        self.assertEqual(len(revision_game.game_rounds), len(revision_game1.game_rounds), 'Len should be equal')

    def test_pages_no_login(self):
        # Arrange

        # Act
        response = self.app_client.get('/', follow_redirects=True)
        # Assert
        self.assertEqual(response.status_code, 200)

        # Act
        response = self.app_client.get('/index', follow_redirects=True)
        # Assert
        self.assertEqual(response.status_code, 200)

        # Pages without login
        # Act
        response = self.app_client.get('/auth/login', follow_redirects=True)
        # Assert
        self.assertEqual(response.status_code, 200)

        # Act
        response = self.app_client.get('/auth/register', follow_redirects=True)
        # Assert
        self.assertEqual(response.status_code, 200)

    def test_pages_login_required(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)

