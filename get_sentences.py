#!/usr/bin/python3

# Obtains sentences with copyright from the ukWac and brWaC corpus to build the Noun Compound Senses (NCS) dataset.

import sys
import re
import os.path
from argparse import ArgumentParser
import pandas as pd
import csv

from input.utils import read_data, read_en_corpus, read_pt_corpus

arg_parser = ArgumentParser(
    description='This script generates the files with the original sentences of the NCS datasets. It requires the ukWaC and/or brWaC corpora to get the sentences with copyright from them.'
)

arg_parser.add_argument(
    '--lang',
    '-l',
    type=str,
    choices=['en', 'pt'],
    help='Language of the dataset: English (en) or Portuguese (pt)',
    required=True,
    default=None
)

arg_parser.add_argument(
    '--corpus',
    '-c',
    type=str,
    required=True,
    help='ukWaC/brWaC corpus. brWaC should be in .conll format. UKWAC as a single file concatenating all the XML files.',
    default=None
)

args = arg_parser.parse_args()
lang = args.lang
corpf = args.corpus

# Input file (sentences and IDs)
if lang == 'en':
    inpf = './input/sentids_en.csv'
elif lang == 'pt':
    inpf = './input/sentids_pt.csv'

# Read sentence ids
nc_ids = pd.read_csv(inpf)

# Get target ids and compounds
target_ids, compounds = read_data(nc_ids, lang)

# Reads corpus
if lang == 'en':
    compounds = read_en_corpus(target_ids, compounds, corpf)
elif lang == 'pt':
    compounds = read_pt_corpus(target_ids, compounds, corpf)

# Output
fname = 'original_sents.csv'
outf = os.path.join('dataset', lang, 'naturalistic', fname)

if os.path.exists(outf):
    ans = 'y'
    ans = input('File %s will be overwritten. Proceed? (y/n) [DEFAULT: y]' %outf)
    if ans == 'n' and ans == 'no':
        exit(0)
        
with open(outf, 'w', newline='') as out:
    # Print head
    writer = csv.writer(out)
    writer.writerow(["compound","compositionality","sentence1","sentence2","sentence3"])
    for c in compounds:
        row = [c, compounds[c]['comp']]
        for sidx in ['sent1', 'sent2', 'sent3']:
            if sidx in compounds[c]:
                row.append(compounds[c][sidx])
        writer.writerow(row)
print('File %s created' %outf)
