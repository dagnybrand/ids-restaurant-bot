# saves the openwebtext dataset to a binary file for training. following was helpful:
# https://github.com/HazyResearch/flash-attention/blob/main/training/src/datamodules/language_modeling_hf.py

import os
from tqdm import tqdm
import numpy as np
import tiktoken
from datasets import load_dataset # huggingface datasets
from datasets import Dataset

import pickle
import random
import argparse
#import bincomb

OUT_DIR = 'jam/data/restaurant-bot'

seqlen = 1024

random.seed(1337)

# number of workers in .map() call
# good number to use is ~order number of cpu cores // 2

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--num-proc', type=int, default=4)

    args = parser.parse_args()

    num_proc = outdir = args.num_proc

    txtfiles = list()

    files_and_directories = os.listdir('tmp/')

    txtfiles = [f'tmp/{f}' for f in files_and_directories if os.path.isfile(os.path.join('tmp/', f))]

    dataset = load_dataset('text', data_files={'train': txtfiles}, sample_by="document")

    split_dataset = dataset['train'].train_test_split(test_size=0.02, seed=2357, shuffle=True)
    split_dataset['val'] = split_dataset.pop('test') # rename the test split to val

    # we now want to tokenize the dataset. first define the encoding function (gpt2 bpe)
    enc = tiktoken.get_encoding("gpt2")

    enc_fn = tiktoken.Encoding(
        name="gpt2-restaurant-bot",
        pat_str=enc._pat_str,
        mergeable_ranks=enc._mergeable_ranks,
        special_tokens={
            **enc._special_tokens,
            '<|start_fn|>' : 100264,
            '<|end_fn|>' : 100265,
        }
    )

    def process(example):
        ids = enc_fn.encode(example['text'], allowed_special={'<|start_fn|>', '<|end_fn|>'}) # encode_ordinary ignores any special tokens
        ids = ids[:seqlen-1]
        ids.append(enc_fn.eot_token) # add the end of text token, e.g. 50256 for gpt2 bpe
        #if len(ids) < seqlen:
        #    while(len(ids) < seqlen):
        #        ids.append(enc.eot_token)
        #print(f'len {len(ids)}')
        #quit()
        # note: I think eot should be prepended not appended... hmm. it's called "eot" though...
        out = {'ids': ids, 'len': len(ids)}
        print(out)
        return out

    # tokenize the dataset
    tokenized = split_dataset.map(
        process,
        remove_columns=['text'],
        desc="tokenizing the splits",
        num_proc=num_proc,
    )

    # concatenate all the ids in each dataset into one large file we can use for training
    for split, dset in tokenized.items():
        arr_len = np.sum(dset['len'])
        filename = os.path.join('.', f'{OUT_DIR}/{split}.bin')
        dtype = np.uint32 # (can do since enc.max_token_value == 50256 is < 2**16)
        arr = np.memmap(filename, dtype=dtype, mode='w+', shape=(arr_len,))

        print(f"writing {filename}...")
        idx = 0
        for example in tqdm(dset):
            arr[idx : idx + example['len']] = example['ids']
            idx += example['len']
        arr.flush()