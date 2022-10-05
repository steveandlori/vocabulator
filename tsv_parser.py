from collections import namedtuple
from html import escape
import pandas as pd

print('Reading TSV input file...please wait')
df = pd.read_csv('HEB 321_721 Vocab with Examples - Sheet1.tsv', delimiter='\t')
rename_mapping={
    'VIS-ED #':'vocab_no', 
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
    Deck(221, 257),     # 1
    Deck(258, 293),     # 2
    Deck(294, 329),     # 3
    Deck(330, 368),     # 4
    Deck(568, 600),     # 5
    Deck(601, 640),     # 6
    None,               # 7
    Deck(221, 640),     # 8 Vocab Midterm
    Deck(641, 680),     # 9
    Deck(724, 757),     # 10
    Deck(758, 790),     # 11
    Deck(791, 823),     # 12
    None,               # 13
    Deck(824, 856),     # 14
    Deck(857, 922),     # 15
    Deck(641, 922),     # Vocab final exam
]

filename = 'vocab_data.js'
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
    fout.write('\nlet all_decks = [')
    for deck in decks_to_build:
        if deck:
            fout.write(f'\n   vocab_{deck.min_index}_{deck.max_index},')
        else:
            fout.write(f'\n   null,')
    fout.write('\n]')
    fout.write('\n')

print(f'FINISHED - output in {filename}')