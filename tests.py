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
        db.session.add(user)
        db.session.commit()
        user_dictionary = Dictionary(dictionary_name='dictionary', user_id=user.id)
        db.session.add(user_dictionary)
        db.session.commit()
        for i in range(50):
            word_i = Word(spelling=f'spelling{i}', definition=f'definition{i}', dictionary_id=user_dictionary.id)
            db.session.add(word_i)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_db(self):
        # Arrange
        # Act
        user = User.query.filter_by(username='Test').first()
        # Assert
        self.assertIsNotNone(user, 'User could not be None')
        self.assertEqual(user.username, 'Test', 'Username should be \'Test\'')

    def test_user_dictionary(self):
        # Arrange
        current_user = User.query.filter_by(username='Test').first()
        # Act
        user_dictionary = Dictionary.query.filter_by(user_id=current_user.id).first()
        # Assert
        self.assertIsNotNone(user_dictionary, 'User dictionary should not be None')
        self.assertEqual(user_dictionary.dictionary_name, 'dictionary', 'Dictionary name should be \'dictionary\'')

    def test_current_game(self):
        # Arrange
        word_limit = 10
        round_i = randint(0,9)
        game_type = GameType.FindSpelling
        words_query = Word.query.order_by(func.random()).all()
        revision_game = GameGenerator.generate_game(words_query, game_type, word_limit)
        current_user = User.query.filter_by(username='Test').first()
        round1 = revision_game.game_rounds[round_i]
        revision_game_entry = CurrentGame()
        revision_game_entry.game_type = game_type.name
        revision_game_entry.game_data = json.dumps(revision_game.to_json())
        revision_game_entry.user_id = current_user.id
        revision_game_entry.total_rounds = revision_game.total_rounds
        revision_game_entry.current_round = 0
        db.session.add(revision_game_entry)
        db.session.commit()

        # Act
        json_rounds = json.loads(revision_game_entry.game_data)
        loaded_round = GameRound(json.loads(json_rounds['game_rounds'][round_i]))

        # Assert
        self.assertIsNotNone(revision_game.game_rounds, 'Game rounds should not be None')
        self.assertEqual(len(revision_game.game_rounds), word_limit)
        self.assertEqual(len(json_rounds['game_rounds']), word_limit)
        self.assertEqual(loaded_round.value,
                         round1.value,
                         f'Value should be '
                         f'\'{round1.value}\' '
                         f'not \'{loaded_round.value}\'')
        for i in range(4):
            self.assertEqual(loaded_round.answers[i],
                             round1.answers[i],
                             f'Answer should be '
                             f'\'{round1.answers[i]}\' '
                             f'not \'{loaded_round.answers[i]}\'')
        self.assertEqual(loaded_round.correct_index,
                         round1.correct_index,
                         f'Correct_index should be '
                         f'\'{round1.correct_index}\' not \'{loaded_round.correct_index}\'')

        self.assertEqual(loaded_round.correct_answer,
                         round1.correct_answer,
                         f'Correct_answer should be '
                         f'\'{round1.correct_answer}\' '
                         f'not \'{loaded_round.correct_answer}\'')

        self.assertEqual(loaded_round.learning_index_id,
                         round1.learning_index_id,
                         f'Learning_index_id should be '
                         f'\'{round1.learning_index_id}\' '
                         f'not \'{loaded_round.learning_index_id}\'')

        self.assertEqual(loaded_round.learning_index_value,
                         round1.learning_index_value,
                         f'Learning_index_value should be '
                         f'\'{round1.learning_index_value}\' '
                         f'not \'{loaded_round.learning_index_value}\'')

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

