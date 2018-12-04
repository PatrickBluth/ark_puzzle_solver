from timeit import default_timer as timer

import itertools
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


def generate_passphrases(desired_address):
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
            raise ValueError('Could not match any words to clue: {}. Please make sure the clue was entered correctly.'.format(key_list[i]))

    total_calculations = 1
    for word_list in possible_words:
        total_calculations *= len(word_list)
    print('Total number of passphrases to try: {}'.format(total_calculations))

    set_network(Mainnet)
    calculations_counter = 0
    milestone = 0

    for words in itertools.product(*possible_words):
        passphrase = " ".join(words)
        calculations_counter += 1
        if calculations_counter - milestone >= 200000:
            print("{} calculations complete".format(calculations_counter))
            milestone = calculations_counter
        if address_from_passphrase(passphrase) == desired_address:
            return passphrase

    return 'No match found.'


def main():
    while True:
        try:
            desired_address = input('Enter the desired address.')
            validate_address(desired_address)
        except ValueError:
            print('Invalid address. Please double check the target address and try again.')
        else:
            break
    start_time = timer()
    passphrase = generate_passphrases(desired_address)
    print('The passphrase is: {}'.format(passphrase))
    end_time = timer()
    print('Total time elapsed: {} s'.format(round(end_time - start_time, 2)))


#AWRdo3zQ9gPeiUEAbogMNGrEBoixPzdowy



main()
