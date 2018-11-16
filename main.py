import itertools


def key_list_bip9_match(key_word, bip39_word):
    if len(key_word) != len(bip39_word):
        return False
    for idx,letter in enumerate(key_word):
        if letter != '_':
            if letter != bip39_word[idx]:
                return False
    return True


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
        if key_list_bip9_match(key_list[i], word):
            possible_words[i].append(word)

res = [' '.join(str(y) for y in x) for x in itertools.product(*possible_words)]
print(len(res))

f = open('passphrases.txt', 'w')
for line in res:
    f.write(str(line))
    f.write('\n')
f.close()


