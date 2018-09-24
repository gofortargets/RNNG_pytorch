# coding=utf-8
from collections import Counter
from typing import List

from torchtext.data import Field
from torchtext.vocab import Vocab
from nltk.grammar import Production

def NP(production: Production):
    return 'NP(' + str(production) + ')'

SHIFT = 'SHIFT'
REDUCE = 'REDUCE'
train_grammar_file = './data/train_grammar.txt'

class ActionRuleField(Field):
    def __init__(self, nonterm_field: Field, productions: List[Production],  **kwargs) -> None:
        unk_token = kwargs.pop('unk_token', None)
        pad_token = kwargs.pop('pad_token', None)
        super().__init__(unk_token=unk_token, pad_token=pad_token, **kwargs)
        self.nonterm_field = nonterm_field
        self.productions = productions

    def build_vocab(self, *args, **kwargs):
        specials = [REDUCE, SHIFT]
        for prod in self.productions:
            specials.append(NP(prod))
        self.vocab = Vocab(Counter(), specials=specials)

    # def numericalize(self, arr, **kwargs) -> Variable:
    #     arr = [[self._actionstr2id(s) for s in ex] for ex in arr]
    #     old_use_vocab = self.use_vocab  # type: ignore
    #     self.use_vocab = False
    #     arr = super().numericalize(arr, **kwargs)
    #     self.use_vocab = old_use_vocab
    #     return arr
    #
    # def _actionstr2id(self, s: str) -> int:
    #     if s in self.vocab.stoi:
    #         return self.vocab.stoi[s]
    #     # must be an unknown NT action, so we map it to NT(<unk>)
    #     action = NT(self.nonterm_field.unk_token)
    #     assert action in self.vocab.stoi
    #     return self.vocab.stoi[action]