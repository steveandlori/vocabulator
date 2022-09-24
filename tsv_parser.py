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
    'English Translation with Hebrew Vocab Word':'mixed_example'
}

df.rename(columns=rename_mapping, inplace=True)
df.fillna('', inplace=True)
print(df.columns.tolist())
print()

Deck = namedtuple('Deck', ['min_index', 'max_index'])
decks_to_build = [
    Deck(221, 257),
    Deck(258, 293),
    Deck(294, 329),
    Deck(330, 368),
    Deck(568, 600),
]

filename = 'vocab_data.js'
with open(filename, encoding='utf-8', mode='w') as fout:
    for deck in decks_to_build:
        print(f'Processing data for vocab_{deck.min_index}_{deck.max_index}')
        subset_df = df.query(f"vocab_no >= {deck.min_index} and vocab_no <= {deck.max_index}")
        fout.write(f'\nlet vocab_{deck.min_index}_{deck.max_index} = [')
        for term in subset_df.itertuples(index=False, name='Term'):
            fout.write(f'\n   ["{term.vocab}", "{escape(term.definition)}", "{term.verse}<br>{term.hebrew_example}", "{term.verse}<br>{term.mixed_example}", "🧠{escape(term.mnemonic)}"],')
        fout.write('\n]')

    fout.write('\n')
    fout.write('\nlet all_decks = [')
    fout.write('\n   null,')
    for deck in decks_to_build:
        fout.write(f'\n   vocab_{deck.min_index}_{deck.max_index},')
    fout.write('\n]')
    fout.write('\n')

print(f'FINISHED - output in {filename}')