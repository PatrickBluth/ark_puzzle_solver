from functools import partial
from timeit import default_timer as timer

import itertools
import multiprocessing as mp

from crypto.configuration.network import set_network
from crypto.identity.address import address_from_passphrase
from crypto.identity.address import validate_address
from crypto.networks.mainnet import Mainnet


def key_list_bip39_match(key_word, bip39_word):
    if len(key_word) != len(bip39_word):
        return False
    for idx, letter in enumerate(key_word):
        if letter != '_':
            if letter != bip39_word[idx]:
                return False
    return True


def generate_possible_words():
    f = open('bip39_words.txt')
    bip39 = f.readlines()
    f.close()
    bip39 = [w.replace('\n', '') for w in bip39]

    f = open('clues.txt')
    key_list = f.readlines()
    f.close()
    key_list = [w.replace('\n', '') for w in key_list]

    if len(key_list) != 12:
        raise ValueError('Please make sure "clues.txt" only has 12 words, one on each line.')

    possible_words = [[] for i in range(12)]
    for i in range(12):
        if key_list[i] == '':
            for word in bip39:
                possible_words[i].append(word)
            continue
        for word in bip39:
            if key_list_bip39_match(key_list[i], word):
                possible_words[i].append(word)
        if len(possible_words[i]) == 0:
            raise ValueError(
                'Could not match any words to clue: {}. Please make sure the clue was entered correctly.'.format(
                    key_list[i]))

    total_calculations = 1
    for word_list in possible_words:
        total_calculations *= len(word_list)
    print('Total number of passphrases to try: {}'.format(total_calculations))

    return possible_words


def generate_passphrases(p_count, possible_words, desired_address, quit, found):
    set_network(Mainnet)
    calculations_counter = 0
    milestone = 0
    print('Processes {} started.'.format(p_count))

    if not quit.is_set():
        for words in itertools.product(*possible_words):
            if quit.is_set():
                break
            passphrase = " ".join(words)
            if p_count == 0:
                calculations_counter += 1
                if calculations_counter - milestone >= 200000:
                    print("{} calculations complete on each process".format(calculations_counter))
                    milestone = calculations_counter
            if address_from_passphrase(passphrase) == desired_address:
                print('Passphrase found: {}'.format(passphrase))
                found.set()
                break
        print('Processes {} closed.'.format(p_count))


if __name__ == "__main__":
    while True:
        try:
            desired_address = input('Enter the desired address.')
            validate_address(desired_address)
        except ValueError:
            print('Invalid address. Please double check the target address and try again.')
        else:
            break

    start_time = timer()

    possible_words = generate_possible_words()
    possible_words_longest_section = possible_words[0]
    for i in range(1, len(possible_words)):
        if len(possible_words[i]) > len(possible_words[i - 1]):
            possible_words_longest_section = possible_words[i]

    num_parts = 4
    part_size = len(possible_words_longest_section) // num_parts
    possible_words_bits = []

    for i in range(num_parts):
        bit = possible_words.copy()
        if i == num_parts - 1:
            bit[-1] = possible_words_longest_section[part_size * i:]
        else:
            bit[-1] = possible_words_longest_section[part_size * i: part_size * (i + 1)]
        possible_words_bits.append(bit)

    quit = mp.Event()
    found = mp.Event()
    pool = mp.Pool(processes=num_parts)
    for p_count, elm in enumerate(possible_words_bits):
        p = mp.Process(target=generate_passphrases, args=(p_count, elm, desired_address, quit, found))
        p.start()
    found.wait()
    quit.set()

    end_time = timer()
    print('Total time elapsed: {} s'.format(round(end_time - start_time, 2)))

# AWRdo3zQ9gPeiUEAbogMNGrEBoixPzdowy
