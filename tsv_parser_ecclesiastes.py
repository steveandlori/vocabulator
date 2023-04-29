from collections import namedtuple
from html import escape
import pandas as pd

print('Reading TSV input file...please wait')
df = pd.read_csv('HEB 722 Ecclesiastes Vocab - main.tsv', delimiter='\t')
rename_mapping={
    'Vocab':'vocab',
    'Definition':'definition',
    'Mnemonic 🧠':'mnemonic',
    'Type':'word_type',
    'Verse':'verse',
    'Hebrew Example':'hebrew_example',
    'English Translation with Hebrew Vocab Word':'mixed_example',
    'Picture':'picture',
}

df.rename(columns=rename_mapping, inplace=True)
df.fillna('', inplace=True)
print(df.columns.tolist())
print()

Deck = namedtuple('Deck', ['min_index', 'max_index'])
decks_to_build = [
    None,    
    Deck(2001, 2020),    # 1
    Deck(2021, 2040),    # 2
    Deck(2041, 2060),    # 3
    Deck(2061, 2080),    # 4
    Deck(2081, 2100),    # 5
    Deck(2101, 2120),    # 6
    Deck(2121, 2140),    # 7
    Deck(2141, 2160),    # 8
    Deck(2161, 2180),    # 9
    Deck(2181, 2200),    # 10
    Deck(2201, 2220),    # 11
    Deck(2221, 2240),    # 12
    Deck(2241, 2260),    # 13
    Deck(2261, 2280),    # 14
    Deck(2281, 2300),    # 15
    Deck(2301, 2320),    # 16
    Deck(2321, 2340),    # 17
    Deck(2341, 2360),    # 18
    Deck(2361, 2380),    # 19
    Deck(2381, 2400),    # 20
    Deck(2421, 2420),    # 21
]

filename = 'vocab_data_ecclesiastes.js'
with open(filename, encoding='utf-8', mode='w') as fout:
    for deck in decks_to_build:
        if deck:
            print(f'Processing data for vocab_{deck.min_index}_{deck.max_index}')
            subset_df = df.query(f"vocab_no >= {deck.min_index} and vocab_no <= {deck.max_index}")
            fout.write(f'\nlet vocab_{deck.min_index}_{deck.max_index} = [')
            for term in subset_df.itertuples(index=False, name='Term'):
                mnemonic_fmt = '' if term.mnemonic.strip() == '' else f"🧠 {escape(term.mnemonic)}"
                fout.write(f'\n   ["{term.vocab}", "{escape(term.definition)}", "{term.verse}<br>{term.hebrew_example}", "{term.verse}<br>{term.mixed_example}", "{mnemonic_fmt}", "{term.picture}"],')
            fout.write('\n]')
            fout.write('\n')
        else: # empty slot 
            pass

    fout.write('\n')
    fout.write('\nlet ecclesiastes_decks = [')
    for deck in decks_to_build:
        if deck:
            fout.write(f'\n   vocab_{deck.min_index}_{deck.max_index},')
        else:
            fout.write(f'\n   null,')
    fout.write('\n]')
    fout.write('\n')

print(f'FINISHED - output in {filename}')