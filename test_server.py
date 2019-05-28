import server
import unittest

from model import connect_to_db
from textprocessor import (remove_irrelevant_characters, make_unique_word_set,
                    make_bigrams, make_bigram_freq_dict)

class TestPythonFunctions(unittest.TestCase):

    def test_remove_irrelevant_characters(self):
        self.assertEqual(remove_irrelevant_characters('a?b.c!d…e,f;g:h*i_j"k()l“”m‘n--op—q'),
            'abcdefghijklmn op q')


    def test_make_unique_word_set(self):
        self.assertEqual(make_unique_word_set("Hey, you. You are great!"), 
            {"hey", "you", "are", "great"})


    def test_make_bigrams(self):
        self.assertEqual(make_bigrams("Hey, you. Yes--you! You are great. You are awesome."), 
           [('Hey', ','), (',', 'you'), ('you', '.'), ('.', 'Yes'), ('Yes', '--'), 
           ('--', 'you'), ('you', '!'), ('!', 'You'), ('You', 'are'), ('are', 'great'), 
           ('great', '.'), ('.', 'You'), ('You', 'are'), ('are', 'awesome'), ('awesome', '.')])


    def test_make_bigram_freq_dict(self):
        self.assertEqual(make_bigram_freq_dict([('Hey', ','), (',', 'you'), ('you', '.'), 
            ('.', 'Yes'), ('Yes', '--'), ('--', 'you'), ('you', '!'), ('!', 'You'), 
            ('You', 'are'), ('are', 'great'), ('great', '.'), ('.', 'You'), 
            ('You', 'are'), ('are', 'awesome'), ('awesome', '.')]), 
            {('You', 'are'): 2, ('are', 'great'): 1, ('are', 'awesome'): 1})


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    def setUp(self):
        
        self.client = server.app.test_client()
        connect_to_db(server.app)


    def test_index(self):
        """Make sure index page returns correct HTML."""

        result = self.client.get('/')
        self.assertIn(b'anachronism finder!', result.data)


    def test_word_search(self):

        result = self.client.get('/word-search')
        self.assertIn(b'2500 characters', result.data)


    def test_bigram_search(self):

        result = self.client.get('/bigram-search')
        self.assertIn(b'input a bigram', result.data)


    def test_show_corpus(self):

        result = self.client.get('/corpus')
        self.assertIn(b'Currently, our corpus', result.data)


    def test_show_methodology(self):

        result = self.client.get('/methodology')
        self.assertIn(b'Kowal', result.data)


if __name__ == '__main__':
    unittest.main()



