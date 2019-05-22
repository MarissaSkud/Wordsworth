import server
import unittest

class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    def test_index(self):
        """Make sure index page returns correct HTML."""

        client = server.app.test_client()
        result = client.get('/')
        self.assertIn(b'anachronism finder!', result.data)


if __name__ == '__main__':
    unittest.main()