from collections import namedtuple
from html import escape
import pandas as pd

print('Reading TSV input file...please wait')
df = pd.read_csv('Hebrew High-Frequency Words.tsv', delimiter='\t')
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
    Deck(1001, 1020),    # 1
    Deck(1021, 1040),    # 2
    Deck(1041, 1060),    # 3
    Deck(1061, 1080),    # 4
    Deck(1081, 1100),    # 5
    Deck(1101, 1120),    # 6
    Deck(1121, 1140),    # 7
    Deck(1141, 1160),    # 8
    Deck(1161, 1180),    # 9
    Deck(1181, 1200),    # 10
    Deck(1201, 1220),    # 11
    Deck(1221, 1240),    # 12
    Deck(1241, 1260),    # 13
    Deck(1261, 1280),    # 14
    Deck(1281, 1300),    # 15
    Deck(1301, 1320),    # 16
    Deck(1321, 1340),    # 17
    Deck(1341, 1360),    # 18
    Deck(1361, 1380),    # 19
    Deck(1381, 1400),    # 20
    Deck(1401, 1418),    # 21
]

filename = 'vocab_data_highfreq.js'
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
    fout.write('\nlet highfreq_decks = [')
    for deck in decks_to_build:
        if deck:
            fout.write(f'\n   vocab_{deck.min_index}_{deck.max_index},')
        else:
            fout.write(f'\n   null,')
    fout.write('\n]')
    fout.write('\n')

print(f'FINISHED - output in {filename}')