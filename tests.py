#!/usr/bin/env python
# !/usr/bin/env python -W ignore::DeprecationWarnin

import unittest
from app import create_app, db
from app.models import Word
from appmodel.GameManager import GameManager
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class WordModelCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

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

    def test_game_manager(self):

        # Arrange
        game_manager = GameManager()
        # Act
        words_limit = 5
        list1 = game_manager.get_game_rounds(words_limit)
        list2 = game_manager.get_game_rounds(words_limit)

        # Assert
        self.assertNotEqual(list1, list2, 'Cannot be equal')
        self.assertEqual(len(list1), words_limit, 'Len of game should be equal')
        self.assertEqual(len(list2), words_limit, 'Len of game should be equal')


if __name__ == '__main__':
    unittest.main(verbosity=2)

