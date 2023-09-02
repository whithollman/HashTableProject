# HashTableProject
This project involves creating a hash table implementation to build a concordance table from a given text file. A concordance table maps words to the line numbers on which they appear in the text.

# Key Features:
1. Hash Table Implementation: The core of this project was to complete the implementation of a hash table, which used open addressing with quadratic probing for collision resolution. The 'hash function' converts words into hash values, which determine their positions within the hash table.
2. Insert Words: Words from the input file 'result_file.txt' into the hash table, each word inserted was linked to a line number where it occurred. If collusions did occur, the program used quadratic probing to the next available slot in the hash table.
3. Load Factor & Resizing: The hash table would keep track of it's own load factor, which is a ratio of occupied slots to total slots. When the load factor exceeded >0.5, the hash table would resize itself. Double it's original size to accommodate more data and reduce collision probabilities.
4. Processing 'Stop Words': Stop words file ‘stop_words.txt’ is a file that contains words that should be ignored during the concordance process (hence the non-obvious title of the tile). These particular words are inserted into a separate hash table, and the stop words that match the ‘result_file.txt’, are ignored. 
5. Concordance Table: This  table crates a concordance table that maps non-stop words to the line numbers in which they appear. This table is implemented through the structure of the hash table. 
6. Testing: Tests are created through ‘unittest’ library which ensured the correct functionality of the hash table and all of its methods. Mocking is also used to simulate the file reading and printing for testing purposes.
7. Horner’s Rule for Hashing: The hash function for converting words to hash values uses Horner’s Rule, which effectively calculates the hash values based on characters in the words. .

# Overall
The project contains data structures, file processing, testing and creates a functional hash table with concordance table system for analyzing text data.
