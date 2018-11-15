f = open('bip39_words.txt')
bip39 = f.readlines()
f.close()
bip39 = [w.replace('\n', '') for w in bip39]

while True:
    print('Enter the given letters for each word. Enter a missing letter with a "_" key.\n'
          'For example: MODIFY ==> M_D_FY')
    print('Enter all 12 words one at a time. Press enter after entering each word.')
    key_list = []
    for i in range(12):
        x = input('')
        key_list.append(x)
    print('Provided words: {}'.format(key_list))
    if input('Continue? Y/n').lower().strip() != 'n':
        break

