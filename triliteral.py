import argparse
import collections
import dataclasses
import itertools
import os.path
import re
import sys


args = argparse.Namespace()
variables = collections.defaultdict(int)
script = None
LATIN = dict(
    values=dict(
        A=1, B=2, G=3, D=4, H=5, E=5, U=6, V=6, W=6, Z=7, C=8, Ch=8, T=9,
        I=10, J=10, Y=10, K=20, L=30, M=40, N=50, S=60, X=60, O=70, F=80, P=80, Ph=80, Ts=90, Tz=90,
        Q=100, R=200, Sh=300, Th=400, K_=500, M_=600, N_=700, P_=800, Ph_=800, Ts_=900, Tz_=900,
    ),
    vowels={'': 0, 'A': 1, 'E': 1, 'U': 2, 'I': 3},
    ext='.tlt',
)
ARABIC=dict(
    values=dict(
        ا=1, ب=2, ج=3, د=4, ه=5, و=6, ز=7, ح=8, ط=9,
        ي=10, ك=20, ل=30, م=40, ن=50, س=60, ع=70, ف=80, ص=90,
        ق=100, ر=200, ش=300, ت=400, ث=500, خ=600, ذ=700, ض=800, ظ=900, غ=1000,
    ),
    vowels={'': 0, 'ا': 1, 'و': 2, 'ي': 3},
    ext='.ثلث',
)
HEBREW=dict(
    values=dict(
        א=1, ב=2, ג=3, ד=4, ה=5, ו=6, ז=7, ח=8, ט=9,
        י=10, כ=20, ל=30, מ=40, נ=50, ס=60, ע=70, פ=80, צ=90,
        ק=100, ר=200, ש=300, ת=400, ך=500, ם=600, ן=700, ף=800, ץ=900,
    ),
    vowels={'': 0, 'א': 1, 'ה': 1, 'ו': 2, 'י': 3},
    ext='.תלת',
)


def trace(s):
    if args.trace:
        print(s)


def parse(path):
    with open(path, 'r') as f:
        return [w for line in f for w in line.split()]


def unpack(word):
    vowels = script['vowels']
    vowels_re = r'([^' + ''.join(vowels.keys()) + r'])'
    parts = re.split(vowels_re, word.upper())
    root = "".join(parts[1::2])
    stem = int("".join(str(vowels.get(c[:1], c[:1])) for c in parts[4::-2]), 4)
    return root, stem


def gem(word):
    acc = 0
    word = word.upper() + '_'
    values = script['values']
    while word and word != '_':
        for i in 3, 2, 1:
            c = word[:i].title()
            if c in values:
                break
        word = word[i:]
        acc += values[c]
    return acc


def degem(n):
    sv, sw = script['values'], script['vowels']
    vowels, consonants = [], []
    m = n
    while m > 0:
        for c, v in reversed(sv.items()):
            if (c[-1] != '_' or not consonants) and (c + '_' not in sv or consonants) and v <= m:
                m -= v
                (vowels if c in sw else consonants)[:0] = (c[:-1] if c[-1] == '_' else c)
                break
    r = ''.join(itertools.chain.from_iterable(itertools.zip_longest(vowels, consonants, fillvalue='')))
    if script is LATIN:
        r = r.replace('TSh', 'CASh')
    assert gem(r) == n, (n, r, gem(r))
    return r


def recode(word, to):
    out = ''
    sv, sw = script['values'], script['vowels']
    tv, tw = to['values'], to['vowels']
    word = ''.join(c for c in word.upper() if c in sv) + '_'
    while word and word != '_':
        for i in 3, 2, 1:
            c = word[:i].title()
            if c in sv:
                break
        word = word[i:]
        x = sv[c]
        y = sw.get(c, 0)
        try:
            out += next(k for k, v in tv.items() if v == x and tw.get(k, 0) == y)
        except StopIteration:
            raise Exception(f"can't recode '{c}' to {args.recode}")
    return out


class State:
    def __init__(self, program):
        self.code = program
        self.wv = ''
        self.root = ''
        self.pc = 0
        self.vs = collections.defaultdict(str)

    def eval(self):
        while self.pc < len(self.code):
            word, self.pc = self.code[self.pc], self.pc + 1
            root, stem = unpack(word)
            op = OPS[stem]
            trace(f"{word=}: {None if op is None else op.__name__}({root}={self.vs[root]})")
            if op is not None:
                self.root = root
                op(self)
            if op is not with_:
                self.wv = ''

    def get(self):
        return self.vs[self.root]

    def get2(self):
        return self.vs[self.wv or self.root], self.vs[self.root]

    def set(self, x):
        self.vs[self.root] = x


def quot(state):
    state.set(state.code[state.pc])
    state.pc += 1


def clr(state):
    state.set('')


def with_(state):
    state.wv = state.root


def load(state):
    ww, _ = state.get2()
    state.set(ww)


def store(state):
    state.vs[state.wv or state.root] = state.get()


def swap(state):
    state.vs[root], state.vs[state.wv or state.root] = state.get2()


def cat(state):
    ww, cw = state.get2()
    if script is LATIN and cw[-1:].upper() == 'T' and ww[:1].upper() in {'S', 'Z'}:
        y = cw[:-1] + 'CA' + ww
    else:
        y = cw + ww
    assert gem(y) == gem(cw) + gem(ww), (cw, ww)
    state.set(y)


def sub(state):
    ww, cw = state.get2()
    state.set(degem(max(0, gem(cw) - gem(ww))))


def mul(state):
    ww, cw = state.get2()
    state.set(degem(gem(cw) * gem(ww)))


def div(state):
    ww, cw = state.get2()
    state.set(degem(gem(cw) // gem(ww)))


def mod(state):
    ww, cw = state.get2()
    state.set(degem(gem(cw) % gem(ww)))


def hop(state):
    word = state.get()
    n = gem(word)
    state.pc = max(0, state.pc - n)
    trace(f"-- hop {n=}: {state.pc=}")


def skip(state):
    word = state.get()
    n = gem(word)
    state.pc += n
    trace(f"-- skip {n=}: {state.pc=}")


def jump(state):
    word = state.get()
    n = gem(word)
    state.pc = n
    trace(f"-- jump {n=}")


def land(state):
    state.set(degem(state.pc))


def gt(state):
    ww, cw = state.get2()
    state.set(degem(1 if gem(cw) > gem(ww) else 0))


def lt(state):
    ww, cw = state.get2()
    state.set(degem(1 if gem(cw) < gem(ww) else 0))


def eq(state):
    ww, cw = state.get2()
    state.set(degem(1 if gem(cw) == gem(ww) else 0))


def neq(state):
    ww, cw = state.get2()
    state.set(degem(1 if gem(cw) != gem(ww) else 0))


def inc(state):
    cw = state.get()
    state.set(degem(gem(cw) + 1))


def dec(state):
    cw = state.get()
    state.set(degem(max(0, gem(state.get()) - 1)))


def not_(state):
    state.set(degem(0 if state.get() else 1))


def and_(state):
    ww, cw = state.get2()
    state.set(degem(1 if cw and ww else 0))


def peek(state):
    word = state.get()
    n = gem(word)
    trace(f"peek {n=}")
    state.set(state.code[n] if n < len(state.code) else '')


def poke(state):
    ww, cw = state.get2()
    n = gem(ww)
    if n < len(state.code):
        trace(f"poke {n=}: {state.code[n]}->{cw}")
        state.code[n] = cw
        state.set(degem(1))
    else:
        trace(f"failed poke {n=}")
        state.set(degem(0))


def rint(state):
    n = int(input())
    state.set(degem(n))


def wint(state):
    word = state.get()
    n = gem(word)
    print(n, flush=True)


def rword(state):
    word = input()
    state.set(word)


def wword(state):
    word = state.get()
    print(word, flush=True)


def rchar(state):
    n = sys.stdin.read(1)
    state.set(degem(ord(n) if n else 0))


def wchar(state):
    word = state.get()
    n = gem(word)
    sys.stdout.write(chr(n))
    sys.stdout.flush()


OPS = [
    None, quot, clr, with_,
    load, store, swap, cat,
    sub, mul, div, mod,
    hop, skip, jump, land,
    gt, lt, eq, neq,
    inc, dec, not_, and_,
    peek, poke, rint, wint,
    rword, wword, rchar, wchar,
] + [None, None, None, None] * 8


def recode_p(program, base):
    to = {'arabic': ARABIC, 'hebrew': HEBREW, 'latin': LATIN}[args.recode]
    with open(base + to['ext'], 'w') as out:
        line = []
        for word in program:
            w = recode(word, to)
            if len(' '.join(line + [w])) <= 120:
                line.append(w)
                continue
            ww, line = line, [w]
            x = 120 - len(' '.join(ww))
            q, r = divmod(x, len(ww) - 1)
            for i, w in enumerate(ww):
                out.write(' ' * (0 if i == 0 else q + 2 if i <= (r + 1) else q + 1) + w)
            out.write('\n')
        out.write(' '.join(line) + '\n')


def run(path):
    global script
    base, ext = os.path.splitext(path)
    script = {s['ext']: s for s in (ARABIC, HEBREW, LATIN)}[ext]
    program = parse(path)
    if args.recode:
        recode_p(program, base)
        return
    State(program).eval()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script")
    parser.add_argument("--recode", choices=['arabic', 'hebrew', 'latin'])
    parser.add_argument("--trace", action='store_true')
    parser.parse_args(namespace=args)
    run(args.script)


if __name__ == "__main__":
    main()
