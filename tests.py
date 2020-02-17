import json
import unittest

from sqlalchemy import func
from random import randint
from app import create_app, db
from app.models import Word, User, Dictionary, CurrentGame
from appmodel.game_generator import GameGenerator
from appmodel.game_round import GameRound
from appmodel.game_type import GameType
from appmodel.revision_game import RevisionGame
from config import Config
from flask_login import login_user, logout_user, current_user


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
        user = User(username='Test')
        user.set_password('Test')
        db.session.add(user)
        db.session.commit()
        user_dictionary = Dictionary(dictionary_name='dictionary', user_id=user.id)
        db.session.add(user_dictionary)
        db.session.commit()
        for i in range(50):
            word_i = Word(spelling=f'spelling{i}', definition=f'definition{i}', dictionary_id=user_dictionary.id)
            db.session.add(word_i)
        db.session.commit()

        # self.login_test_user(user)
    
        # Add entry to current_game table
        word_limit = 10
        game_type = GameType.FindSpelling
        words_query = Word.query.order_by(func.random()).all()
        self.revision_game = GameGenerator.generate_game(words_query, game_type, word_limit)
        curr_user = User.query.filter_by(username='Test').first()
        self.round_index = randint(0, 9)
        self.round_i = self.revision_game.game_rounds[self.round_index]
        revision_game_entry = CurrentGame()
        revision_game_entry.game_type = game_type.name
        revision_game_entry.game_data = json.dumps(self.revision_game.to_json())
        revision_game_entry.user_id = curr_user.id
        revision_game_entry.total_rounds = self.revision_game.total_rounds
        revision_game_entry.current_round = 0
        db.session.add(revision_game_entry)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_db(self):
        with self.app_client:
            # Arrange
            self.login_test_user('Test', 'Test')
            # Act
            user = User.query.filter_by(username='Test').first()
            # Assert
            # TODO self.assertEqual(current_user, user, 'User should Test')
            self.assertIsNotNone(current_user, 'User could not be None')
            # TODO self.assertEqual(current_user.username, 'Test', 'Username should be \'Test\'')

    def test_user_dictionary(self):
        # Arrange
        curr_user = User.query.filter_by(username='Test').first()
        # Act
        user_dictionary = Dictionary.query.filter_by(user_id=curr_user.id).first()
        # Assert
        self.assertIsNotNone(user_dictionary, 'User dictionary should not be None')
        self.assertEqual(user_dictionary.dictionary_name, 'dictionary', 'Dictionary name should be \'dictionary\'')

    def test_current_game(self):
        # Arrange
        curr_user = User.query.filter_by(username='Test').first()
        word_limit = 10
        game_type = GameType.FindSpelling
        revision_game_entry = CurrentGame.query.filter_by(user_id=curr_user.id).first()
        # Act
        json_rounds = json.loads(revision_game_entry.game_data)
        loaded_round = GameRound(json.loads(json_rounds['game_rounds'][self.round_index]))

        # Assert
        self.assertEqual(revision_game_entry.game_type, game_type.name, 'Game type not equal')
        self.assertIsNotNone(self.revision_game.game_rounds, 'Game rounds should not be None')
        self.assertEqual(len(self.revision_game.game_rounds), word_limit)
        self.assertEqual(len(json_rounds['game_rounds']), word_limit)
        self.assertEqual(loaded_round.value, self.round_i.value, f'Value should be equal')

        for i in range(4):
            self.assertEqual(loaded_round.answers[i], self.round_i.answers[i], f'Answer should be equal')

        self.assertEqual(loaded_round.correct_index, self.round_i.correct_index, f'Correct_index should be equal')

        self.assertEqual(loaded_round.learning_index_id,
                         self.round_i.learning_index_id,
                         f'Learning_index_id should be equal')

        self.assertEqual(loaded_round.learning_index_value,
                         self.round_i.learning_index_value,
                         f'Learning_index_value should be equal')

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
        self.assertEqual(len(list1.game_rounds), words_limit, 'Len of game should be equal')
        self.assertEqual(len(list2.game_rounds), words_limit, 'Len of game should be equal')

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
        # logout_user()
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
        # Arrange
        user = User.query.filter_by(username='Test').first()
        # login_user(user)
        # Act
        response = self.app_client.get('/dictionaries', follow_redirects=True)
        # Assert
        self.assertEqual(response.status_code, 200)

    def test_dictionaries(self):
        # Arrange
        user = User.query.filter_by(username='Test').first()
        user_dictionary = Dictionary(dictionary_name='new_dictionary', user_id=user.id)
        db.session.add(user_dictionary)
        db.session.commit()
        # Act
        response = self.app_client.post('/check_dictionary_name', data=dict(dictionary_name='new_dictionary'))
        # Assert
        res = json.loads(response.data)
        self.assertFalse(res['name_available'])
        # Act
        response = self.app_client.post('/check_dictionary_name', data=dict(dictionary_name='new_dictionary name'))
        res = json.loads(response.data)
        self.assertTrue(res['name_available'])

    def login_test_user(self, username, password):
        return self.app_client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout_user(self):
        return self.app_client.get('/logout', follow_redirects=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)

