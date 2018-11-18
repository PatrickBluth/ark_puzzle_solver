import itertools
from timeit import default_timer as timer

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


def generate_passphrases(address):
    f = open('bip39_words.txt')
    bip39 = f.readlines()
    f.close()
    bip39 = [w.replace('\n', '') for w in bip39]

    f = open('clues.txt')
    key_list = f.readlines()
    f.close()
    key_list = [w.replace('\n', '') for w in key_list]

    if len(key_list) != 11 or '' in key_list:
        raise ValueError('Please make sure "clues.txt" only has 12 words, one on each line.')

    possible_words = [[] for i in range(12)]
    for i in range(11):
        for word in bip39:
            if key_list_bip39_match(key_list[i], word):
                possible_words[i].append(word)
        if len(possible_words[i]) == 0:
            raise ValueError('Could not match any words to clue "{}". Please make sure the clue was entered correctly.'.format(key_list[i]))

    for word in bip39:
        possible_words[11].append(word)

    # res = [' '.join(str(y) for y in x) for x in itertools.product(*possible_words)]
    set_network(Mainnet)
    for word1 in possible_words[0]:
        for word2 in possible_words[1]:
            for word3 in possible_words[2]:
                for word4 in possible_words[3]:
                    for word5 in possible_words[4]:
                        for word6 in possible_words[5]:
                            for word7 in possible_words[6]:
                                for word8 in possible_words[7]:
                                    for word9 in possible_words[8]:
                                        for word10 in possible_words[9]:
                                            for word11 in possible_words[10]:
                                                for word12 in possible_words[11]:
                                                    passphrase = word1 + ' ' + word2 + ' ' + word3 + ' ' + word4 + ' ' + word5 + ' ' + word6 + ' ' + word7 + ' ' + word8 + ' ' + word9 + ' ' + word10 + ' ' + word11 + ' ' + word12
                                                    # passphrase = ' '.join(str(y) for y in x)
                                                    corresponding_address = address_from_passphrase(passphrase)
                                                    if corresponding_address == address:
                                                        return passphrase

    return None
    # print('Possibilities for each clue:')
    # for line in possible_words:
    #     print(line)



def find_correct_passphrase(desired_address, phassphrases):
    start = timer()
    set_network(Mainnet)
    for passphrase in phassphrases:
        corresponding_address = address_from_passphrase(passphrase)
        if corresponding_address == desired_address:
            end = timer()
            print('total time: {} s'.format(round((end - start), 2)))
            return passphrase
    return None


def main():
    while True:
        try:
            address = input('Enter the desired address.')
            validate_address(address)
        except ValueError:
            print('Invalid address. Please double check the target address and try again.')
        else:
            break
    passphrase = generate_passphrases(address)
    print('The passphrase is: {}'.format(passphrase))
    input('Press enter to quit')
    # print('\nNumber of passphrases to test: {}'.format(len(passphrases)))
    # print('Estimated completion time: {} seconds'.format(round(len(passphrases)/30000), 2))
    # print('Exit and update clues.txt to narrow search, or continue and input target address\n')
    #
    # passphrase = find_correct_passphrase(address, passphrases)
    # print('Passphrase is: {}'.format(passphrase))
    # input('Press enter to quit')


main()
