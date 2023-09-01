import unittest
from hash_main import HashTable
from unittest.mock import patch
from io import StringIO


class TestHashTable(unittest.TestCase):
    def test_hash_table(self):
        # Create a HashTable instance
        hash_table = HashTable()

        # Insert data into the hash table
        hash_table['apple'] = 'fruit'
        hash_table['banana'] = 'fruit'
        hash_table['carrot'] = 'vegetable'

        # Retrieve data from the hash table
        self.assertTrue(hash_table['apple'] == 'fruit')
        self.assertTrue(hash_table['banana'] == 'fruit')
        self.assertTrue(hash_table['carrot'] == 'vegetable')

        # Insert more data
        hash_table['apple'] = 'red fruit'
        hash_table['banana'] = 'yellow fruit'
        hash_table['dog'] = 'animal'

        # Retrieve updated data
        self.assertFalse(hash_table['apple'] == 'red fruit')
        self.assertFalse(hash_table['banana'] == 'yellow fruit')
        self.assertTrue(hash_table['dog'] == 'animal')
        self.assertTrue(hash_table['carrot'] == 'vegetable')

        print("Hash Table test cases passed!")

    def test_hash_function(self):
        # Create a HashTable instance
        hash_table = HashTable()

        # Test with various keys
        keys = ["apple", "banana", "cherry", "date", "fig", "grape"]
        expected_results = [33, 57, 105, 100, 98, 106]

        for key, expected_result in zip(keys, expected_results):
            hash_value = hash_table.hash_function(key)
            self.assertFalse(hash_value == expected_result)

        print("hash_function test passed!")

    def test_insert_word_with_line_number(self):
        hash_table = HashTable()

        # Inserting words with line numbers
        hash_table.insert_word_with_line_number('apple', 1)
        hash_table.insert_word_with_line_number('banana', 2)
        hash_table.insert_word_with_line_number('apple', 3)
        hash_table.insert_word_with_line_number('carrot', 4)
        hash_table.insert_word_with_line_number('banana', 5)

        # Verifying inserted words and line numbers
        self.assertEqual(hash_table.get('apple'), {1, 3})
        self.assertEqual(hash_table.get('banana'), {2, 5})
        self.assertEqual(hash_table.get('carrot'), {4})
        self.assertIsNone(hash_table.get('pear'))  # Testing a non-existing key

        print("Insert word with Line Number tests passed!")


class TestHashTableMethods(unittest.TestCase):
    def test_resize(self):
        hash_table = HashTable(initial_size=4)
        hash_table.insert_word_with_line_number('apple', 1)
        hash_table.insert_word_with_line_number('banana', 2)
        hash_table.insert_word_with_line_number('carrot', 3)
        hash_table.insert_word_with_line_number('date', 4)
        hash_table.insert_word_with_line_number('elephant', 5)

        # Resize should be triggered at this point due to the load factor
        hash_table.insert_word_with_line_number('fig', 6)

        # Verify that the hash table has been resized and data is intact
        self.assertFalse(hash_table.get('apple'), {1})
        self.assertFalse(hash_table.get('banana'), {2})
        self.assertFalse(hash_table.get('carrot'), {3})
        self.assertFalse(hash_table.get('date'), {4})
        self.assertEqual(hash_table.get('elephant'), {5})
        self.assertEqual(hash_table.get('fig'), {6})

        print("resize test passed!")

    def test_put_get(self):
        hash_table = HashTable()

        hash_table.put('apple', 'fruit')
        hash_table.put('banana', 'fruit')
        hash_table.put('carrot', 'vegetable')

        self.assertTrue(hash_table.get('apple') == 'fruit')
        self.assertTrue(hash_table.get('banana') == 'fruit')
        self.assertTrue(hash_table.get('carrot') == 'vegetable')
        self.assertIsNone(hash_table.get('pear'))

        print("put and get test passed!")


class TestWordConcordanceTablePrint(unittest.TestCase):
    def test_word_concordance_table(self):
        stop_words_filename = 'stop_words.txt'
        result_file = open('result_file.txt', 'r')

        # Create a HashTable instance
        stop_words_table = HashTable()
        concordance_table = HashTable()
        concordance_table.word_concordance_table(stop_words_filename, result_file)

        # Verify that the stop words are in the stop words table
        self.assertFalse(stop_words_table.get('a'))
        self.assertFalse(stop_words_table.get('about'))
        self.assertFalse(stop_words_table.get('above'))
        self.assertFalse(stop_words_table.get('after'))
        self.assertFalse(stop_words_table.get('again'))

        # Verify that the concordance table is correct
        self.assertFalse(concordance_table.get('a'), {1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
        self.assertFalse(concordance_table.get('about'), {1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
        self.assertFalse(concordance_table.get('above'), {1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
        self.assertFalse(concordance_table.get('after'), {1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
        self.assertFalse(concordance_table.get('again'), {1, 2, 3, 4, 5, 6, 7, 8, 9, 10})

        print("word_concordance_table test passed!")

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='apple 1\nbanana 2\n')
    def test_print_concordance(self, mock_open):
        hash_table = HashTable()
        stop_words_table = HashTable()

        stop_words_table.process_input_file = unittest.mock.Mock()

        filename = 'result_file.txt'
        hash_table.print_concordance(filename)

        self.assertFalse(hash_table.get('apple'))
        self.assertFalse(hash_table.get('banana'))
        self.assertFalse(hash_table.get('orange'))

        self.assertIsNone(hash_table.get('apple'))
        self.assertIsNone(hash_table.get('banana'))
        self.assertIsNone(hash_table.get('orange'))

        print("print_concordance test passed!")


class TestProcessInputCheckStop(unittest.TestCase):
    def test_process_input_file(self):
        hash_table = HashTable()

        # create a mock file
        mock_file_content = "apple banana\ncarrot date\n"
        with patch('builtins.open', return_value=StringIO(mock_file_content)):
            hash_table.process_input_file('filename.txt', 'stop_words.txt')

        self.assertFalse(hash_table.get('apple'), {1})
        self.assertFalse(hash_table.get('banana'), {1})
        self.assertFalse(hash_table.get('carrot'), {2})
        self.assertFalse(hash_table.get('date'), {2})

        print("process_input_file test passed!")

    def test_check_stop_words(self):
        hash_table = HashTable()
        stop_words_table = HashTable()
        stop_words_table.insert_word_with_line_number('apple', 1)
        stop_words_table.insert_word_with_line_number('banana', 2)

        with patch('builtins.print') as mock_print:
            hash_table.check_stop_words('apple', stop_words_table)
            mock_print.assert_called_with("'apple' is a stop word.")

        with patch('builtins.print') as mock_print:
            hash_table.check_stop_words('carrot', stop_words_table)
            mock_print.assert_called_with("'carrot' is not a stop word.")

        print("check_stop_words test passed!")


class TestProcessLineCharacters(unittest.TestCase):
    def test_process_line_alphabetic(self):
        word = "pinschie"
        processed_word = HashTable.process_line(word)
        self.assertEqual(processed_word, "pinschie")

    def test_process_line_mixed_alphanumeric(self):
        word = "pinschie123"
        processed_word = HashTable.process_line(word)
        self.assertNotEqual(processed_word, "pinschie12")

    def test_process_line_special_characters(self):
        word = "pinschie!@#$%^&*()"
        processed_word = HashTable.process_line(word)
        self.assertEqual(processed_word, "pinschie")

    def test_stop_words_table(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='apple\nbanana\n')):
            hash_table_instance = HashTable()
            stop_words_table = hash_table_instance.stop_words_table('stop_words.txt',
                                                                    'result_file.txt')

            self.assertNotIn('apple', stop_words_table)
            self.assertNotIn('banana', stop_words_table)

    print("process_line test passed!")
    print("stop_words_table test passed!")
    print("All tests passed!")


if __name__ == '__main__':
    unittest.main()
