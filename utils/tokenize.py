import sys
import codecs
import unicodedata
from keras_bert import Tokenizer
from transformers import AutoTokenizer

"""
The HBTokenizer is critical to OneRel.
"""

class HBBioBertTokenizer:
    def __init__(self, cased=True):
        from transformers import AutoTokenizer

        self.tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
        self._cased = cased

    def _normalize(self, text):
        if not self._cased:
            text = unicodedata.normalize('NFD', text)
            text = ''.join([ch for ch in text if unicodedata.category(ch) != 'Mn'])
            text = text.lower()
        return text

    def _tokenize(self, text):
        text = self._normalize(text)
        tokens = ['[CLS]']
        for word in text.strip().split():
            word_pieces = self.tokenizer.tokenize(word)
            for piece in word_pieces:
                tokens.append(piece)
                tokens.append('[unused1]')
        tokens.append('[SEP]')
        return tokens
    
    def encode(self, first):
        tokens = ["[CLS]"] + self._tokenize(first) + ["[SEP]"]
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        segment_ids = [0] * len(token_ids)
        return token_ids, segment_ids

    def tokenize(self, text):
        return self._tokenize(text)


class HBTokenizer(Tokenizer):
    def _tokenize(self, text):
        if not self._cased:
            text = unicodedata.normalize('NFD', text)
            text = ''.join([ch for ch in text if unicodedata.category(ch) != 'Mn'])
            text = text.lower()
        spaced = ''
        for ch in text:
            if ord(ch) == 0 or ord(ch) == 0xfffd or self._is_control(ch):
                continue
            else:
                spaced += ch
        tokens = []
        for word in spaced.strip().split():
            tokens += self._word_piece_tokenize(word)
            tokens.append('[unused1]')
        return tokens


def get_tokenizer(vocab_path):
    token_dict = {}
    with codecs.open(vocab_path, 'r', 'utf8') as reader:
        for line in reader:
            token = line.strip()
            token_dict[token] = len(token_dict)
    return HBBioBertTokenizer(token_dict)
    # return HBTokenizer(token_dict)