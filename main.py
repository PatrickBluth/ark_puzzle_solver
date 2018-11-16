import itertools


def gen_word_possiblities():
    f = open('bip39_words.txt')
    bip39 = f.readlines()
    f.close()
    bip39 = [w.replace('\n', '') for w in bip39]

    f = open('clues.txt')
    key_list = f.readlines()
    f.close()
    key_list = [w.replace('\n', '') for w in key_list]

    possible_words = [[] for i in range(12)]
    for i in range(12):
        for word in bip39:
            if len(word) == len(key_list[i]) and word[0] == key_list[i][0] and word[-1] == key_list[i][-1]:
                possible_words[i].append(word)

    print(possible_words)

    f = open('possible_words.txt', 'w')
    for line in possible_words:
        f.write(str(line))
        f.write('\n')
    f.close()


def gen_passphrace_from_hints():
    f = open('possible_words.txt')

    #res = [' '.join(str(y) for y in x) for x in itertools.product(*possible_words)]


def main():
    while True:
        print('First generate all possible words. Then edit the text file to manually apply any hints.\n '
              'Rerun the program and continue to the second step.')
        ans = input("Press 1 to generate possible words. Press 2 to use updated word list with hints.")
        if ans == 1:
            gen_word_possiblities()
            break
        elif ans == 2:
            gen_passphrace_from_hints()
            break





main()
# for i in range (20):
#     print(res[i])
