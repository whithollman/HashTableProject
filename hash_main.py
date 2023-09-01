from dataclasses import dataclass


class HashTable:
    def __init__(self, initial_size=128):
        self.size = initial_size
        self.slots = [None] * self.size
        self.data = [set() for _ in range(self.size)]
        self.next_slot = None

    def __setitem__(self, key, data_value):
        self.put(key, data_value)

    def __getitem__(self, key):
        return self.get(key)

    def __len__(self):
        return self.size

    def __contains__(self, key):
        return self.get(key) is not None

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.process_input_file)

    def __iter__(self):
        return iter(self.data)

    def hash_function(self, key):
        hash_value = 0
        n = min(len(key), 8)
        self.size = n

        for i in range(n):
            hash_value = hash_value * 31 + ord(key[i])

        return hash_value % len(self.slots)

    def put(self, key, slot):
        hash_value = self.hash_function(key)
        data_value = slot

        if self.slots[hash_value] is not None:
            next_slot = self.rehash(hash_value, len(self.slots))
            while self.slots[next_slot] is not None and self.slots[next_slot] != key:
                next_slot = self.rehash(next_slot, len(self.slots))

            if self.slots[next_slot] is None:
                self.slots[next_slot] = key
                self.data[next_slot] = data_value

            else:
                self.data[next_slot] = data_value  # replace
        else:
            self.slots[hash_value] = key
            self.data[hash_value] = data_value

    def get(self, key):
        start_slot = self.hash_function(key)

        data = None
        stop = False
        found = False
        position = start_slot
        while self.slots[position] is not None and not found and not stop:
            if self.slots[position] == key:
                found = True
                data = self.data[position]
            else:
                position = self.rehash(position, len(self.slots))
                if position == start_slot:
                    stop = True
        return data

    @staticmethod
    def rehash(old_hash, size):
        return (old_hash + 1) % size

    def insert_word_with_line_number(self, key, line_number):
        hash_value = self.hash_function(key)

        if self.slots[hash_value] is None:
            self.slots[hash_value] = key
            self.data[hash_value] = {line_number}

        else:
            if self.slots[hash_value] == key:
                self.data[hash_value].add(line_number)
            else:
                next_slot = self.rehash(hash_value, len(self.slots))
                while self.slots[next_slot] is not None and self.slots[next_slot] != key:
                    next_slot = self.rehash(next_slot, len(self.slots))

                if self.slots[next_slot] is None:
                    self.slots[next_slot] = key
                    self.data[next_slot] = {line_number}
                else:
                    self.data[next_slot].add(line_number)

            load_factor = sum(1 for slot in self.slots if slot is not None) / len(self.slots)
            if load_factor > 0.5:
                self.resize(self.slots)

    def resize(self, next_slot):
        new_size = self.size * 2
        new_slot = [None] * new_size
        new_data = [set() for _ in range(new_size)]
        self.slots = new_slot
        self.data = new_data
        self.size = new_size

        for i in range(self.size):
            if self.slots[1] is not None:
                for line_number in self.data[i]:
                    new_hash_value = self.hash_function(self.slots)
                    if new_slot[new_hash_value] is None:
                        new_slot[new_hash_value] = self.slots[i]
                        new_data[new_hash_value] = {line_number}
                    else:
                        next_slot = self.rehash(new_hash_value, new_size)
                        iteration = 1
                        while new_slot[next_slot] is not None:
                            next_slot = self.rehash(new_hash_value, new_size)
                            iteration += 1
                    new_slot[next_slot] = self.slots[i]
                    new_data[next_slot] = {line_number}

    def check_stop_words(self, word, stop_words_table):
        if stop_words_table.get(word) is not None:
            print(f"'{word}' is a stop word.")
        else:
            new_word = self.process_line(word)
            print(f"'{new_word}' is not a stop word.")

    def word_concordance_table(self, filename, stop_words_table):
        concordance_table = HashTable(self.size)
        concordance_table.process_input_file(filename, stop_words_table)
        filename = 'result_file.txt'

        with open(filename, 'r') as file:
            for line in file:
                parts = line.split()
                word = parts[0]
                line_numbers = [int(num) for num in parts[1:]]

                if word.isalpha():
                    word = word.lower()
                    for line_num in line_numbers:
                        concordance_table.insert_word_with_line_number(word, line_num)

    def print_concordance(self, result_filename):
        pass

    def process_input_file(self, stop_words_filename, result_filename):
        pass

    @staticmethod
    def process_line(word):
        if word.isalpha():
            return word.lower()
        else:
            return ''.join([ch.lower() for ch in word if ch.isalpha()])

    def stop_words_table(self, stop_words_filename, result_filename):
        stop_words_table = HashTable(self.size)
        stop_words_table.process_input_file(stop_words_filename, result_filename)
        return stop_words_table

    print(stop_words_table)


def main():
    initial_size = 128
    hash_table = HashTable(initial_size)
    stop_words_filename = 'stop_words.txt'
    result_filename = 'result_file.txt'
    hash_table.process_input_file(stop_words_filename, result_filename)
    hash_table.print_concordance(result_filename)


if __name__ == "__main__":
    main()


    def process_input_file(self, filename, line_number=1):
        with open(filename, 'r') as file:
            for line in file:
                words = self.process_line(line)
                for word in words:
                    self.insert_word_with_line_number(word, line_number)


    def print_concordance(self, filename, result_filename):
        stop_words_table = HashTable()
        stop_words_table.process_input_file(filename, result_filename)

        with open(filename, 'r') as result_file:
            for line_number, line in enumerate(result_file, start=1):
                words = self.process_line(line)

                if words:
                    non_stop_words = [word for word in words if not stop_words_table.get(word)]
                    if non_stop_words:
                        print('Line {}: {}'.format(line_number, non_stop_words))
