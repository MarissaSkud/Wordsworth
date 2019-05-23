import server
import unittest

from model import connect_to_db

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



