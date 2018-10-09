# def add_dummy_pos(tree):
#     if not isinstance(tree, Tree):
#         return Tree('XX', [tree])
#     return Tree(tree.label(), [add_dummy_pos(t) for t in tree])
#
#
# def get_evalb_f1(evalb_output):
#     lines = reversed(evalb_output.strip().split('\n'))
#     for i in range(20):
#         line = next(lines)
#     return float(line.split()[-1])

# def id2parsetree(tree, id2nonterm, id2word):
#     if not isinstance(tree, Tree):
#         return id2word[tree]
#     children = [id2parsetree(t, id2nonterm, id2word) for t in tree]
#     return Tree(id2nonterm[tree.label()], children)
#
# def actions2treestr(actions, toks, postags = None):
#     ret = ''
#     p = 0
#     for action_tok in actions:
#         if action_tok == 'SHIFT':
#             if postags == None:
#                 ret += toks[p] + ' '
#             else:
#                 ret += '( ' + postags[p] + ' ' + toks[p] + ' ) '
#             p += 1
#         elif action_tok == 'REDUCE':
#             ret += ') '
#         else: #NT
#             ret += action_tok[2:-1] + ' '
#     return ret
from typing import List


def action2treestr(actions: List[str], tokens: List[str], postags: List[str] = None) -> str:
    res = ''
    p = 0
    for action in actions:
        if action == 'SHIFT':
            if postags == None:
                res += tokens[p] + ' '
            else:
                res += '(' + postags[p] + ' ' + tokens[p] + ') '
            p += 1
        elif action == 'REDUCE':
            res += ') '
        else:  # NP (rule)
            prod_split = action[3:-1].partition('->')
            lhs = prod_split[0].strip()
            res += '(' + lhs + ' '
    return res


class ParsingMeter(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.match_num = 0
        self.pred_num = 0
        self.gold_num = 0
        self.error_tree = 0

    @property
    def precision(self):
        if self.match_num == 0: return 0
        assert self.pred_num > 0
        return (self.match_num + 0.0) / self.pred_num

    @property
    def recall(self):
        if self.match_num == 0: return 0
        assert self.gold_num > 0
        return (self.match_num + 0.0) / self.gold_num

    @property
    def f1(self):
        if self.match_num == 0: return 0
        return 2 * self.precision * self.recall / (self.precision + self.recall)

    def update(self, res):
        if res == -1:
            self.error_tree += 1
            return
        self.match_num += res[0]
        self.gold_num += res[1]
        self.pred_num += res[2]
