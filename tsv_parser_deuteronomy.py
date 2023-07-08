from collections import namedtuple
from html import escape
import pandas as pd

print('Reading TSV input file...please wait')
df = pd.read_csv('Deuteronomy_High_Frequency_Words.tsv', delimiter='\t')
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
    Deck(5001, 5020),    # 1
    Deck(5021, 5040),    # 2
    Deck(5041, 5060),    # 3
    Deck(5061, 5080),    # 4
    Deck(5081, 5100),    # 5
    Deck(5101, 5120),    # 6
    Deck(5121, 5140),    # 7
    Deck(5141, 5160),    # 8
    Deck(5161, 5180),    # 9
    Deck(5181, 5200),    # 10
    Deck(5201, 5220),    # 11
    Deck(5221, 5240),    # 12
    Deck(5241, 5260),    # 13
    Deck(5261, 5280),    # 14
    Deck(5281, 5300),    # 15
]

filename = 'vocab_data_deuteronomy.js'
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
    fout.write('\nlet deuteronomy_decks = [')
    for deck in decks_to_build:
        if deck:
            fout.write(f'\n   vocab_{deck.min_index}_{deck.max_index},')
        else:
            fout.write(f'\n   null,')
    fout.write('\n]')
    fout.write('\n')

print(f'FINISHED - output in {filename}')