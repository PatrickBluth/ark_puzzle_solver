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


def generate_passphrases():
    f = open('bip39_words.txt')
    bip39 = f.readlines()
    f.close()
    bip39 = [w.replace('\n', '') for w in bip39]

    f = open('clues.txt')
    key_list = f.readlines()
    f.close()
    key_list = [w.replace('\n', '') for w in key_list]

    if len(key_list) != 12 or '' in key_list:
        raise ValueError('Please make sure "clues.txt" only has 12 words, one on each line.')

    possible_words = [[] for i in range(12)]
    for i in range(12):
        for word in bip39:
            if key_list_bip39_match(key_list[i], word):
                possible_words[i].append(word)
        if len(possible_words[i]) == 0:
            raise ValueError('Could not match any words to clue "{}". Please make sure the clue was entered correctly.'.format(key_list[i]))

    res = [' '.join(str(y) for y in x) for x in itertools.product(*possible_words)]
    return res


def find_correct_passphrase(desired_address, phassphrases):
    set_network(Mainnet)
    for passphrase in phassphrases:
        corresponding_address = address_from_passphrase(passphrase)
        if corresponding_address == desired_address:
            return passphrase
    return None


def main():
    passphrases = generate_passphrases()
    while True:
        try:
            address = input('Enter the desired address.')
            validate_address(address)
        except ValueError:
            print('Invalid address. Please double check the target address and try again.')
        else:
            break
    passphrase = find_correct_passphrase(address, passphrases)
    print('Passphrase is: {}'.format(passphrase))
    input('Press enter to quit')


main()
