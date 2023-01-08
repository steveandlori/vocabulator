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
    Deck(1001, 1020),    # 1
    Deck(1021, 1040),    # 2
    Deck(1041, 1060),    # 3
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