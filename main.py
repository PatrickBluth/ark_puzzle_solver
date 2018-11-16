import itertools


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

    f = open('passphrases.txt', 'w')
    for line in res:
        f.write(str(line))
        f.write('\n')
    f.close()

    print('Update clue list based on provided hints to narrow results.')
    print('Possible words: ')
    for word_list in possible_words:
        print(word_list)
    print('\nTotal number of possible passphrases: {}'.format(len(res)))
    input('\nPress enter to exit')


def main():
    generate_passphrases()


main()
