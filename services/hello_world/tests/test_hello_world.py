from unittest import TestCase
from hello_world.hello_world import hello_world


class HelloWorldTestCase(TestCase):
    def test_hello_world(self):
        self.assertEqual('Hello World', hello_world())
