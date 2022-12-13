Triliteral is a literate, polyglossal, esoteric, homoiconic, concatenative, concurrent, Turing-complete, stack-oriented language based on FALSE and inspired by the *triliteral root* construction common to Semitic languages.
Triliteral programs can be written in the Arabic, Hebrew or (with some loss of fidelity) Latin scripts, though only one at a time; the script used is determined by the file extension: .طرل, .טרל or .trl.

A Triliteral program is a sequence of *words*, separated by whitespace and/or punctuation, where each word is derived from a (usually tri-)consonantal *root* designating a *stack*, modified by a vowel *stem* designating an *operation*, each consonant having a preceding vowel.
The number of available consonants (and thus the number of stacks) depends on the script used, with Triliteral written in Arabic having 25 consonants (hamza not considered a letter) available, Hebrew 18 and Latin 22; in the Semitic scripts these are the letters other than the *matres lectrionis*, whereas in Latin they are the letters other than certain vowels.
The matres lectrionis (full vowels in Latin) are ﺍ, ﻭ and ﻱ in Arabic; א, ה', ו and י in Hebrew, and *aeui* in Latin; however, for the purposes of forming stems, א and ה are considered equivalent, as are a and e in Latin, while the short vowels (which may be designated - entirely optionally - by harakat in Arabic and niqqud in Hebrew, but must be omitted entirely in Latin) are considered together a fourth "vowel"; altogether each script has 4 vowel categories resulting in 4^3 = 64 possible stems.

For purposes of organization the vowels may be considered having the following digit values in a base-4 system: short vowels 0,  ﺍ/א/ה/a/e 1, ﻭ/ו/u 2, and ﻱ/י/i 3, with the *lowest* place value at the *start* of the word (the rightmost position in Arabic and Hebrew, the leftmost in Latin).
For example, the word *aktub* has root KTB and stem a-u, 201 in base 4 (33 in decimal, although this is not used much).
(Note that Triliteral written in the Latin script is case-insensitive, so this could also be written *Aktub*, *aKTuB* etc., with exactly the same meaning.)
Words also have a *numeric* value when used as the object of arithmetic operations, with that value determined (naturally) by *gematria*, adding together the values of the letters (in the common abjadi sequence in Arabic, the Mispar Gadol system in Hebrew, and the Golden Dawn system (*with* digraphs) in Latin) to produce a single value; so, again, *aktub* designates the *number* 1+20+9+6+2 = 38.
Words may have more or fewer than 3 consonants, subject to implementation limits.
Consecutive long vowels are permitted but only the first in each position contribute to the stem; any following contribute only to gematria.
For example, *gematria* is parsed as *-GeMaT(ria)* i.e. root *GMT* and stem *-ea*, where *-* designates an empty position.
The observant will note that this means that any text (for example, this document) can be parsed as a Triliteral program, and that any positive number can be entered; however, Triliteral implementations are required only to support values up to the largest that can be entered without repeated long vowels; for example, *ithithitz* in Latin script (gematria 1630); likewise יציציץ (1110) in Hebrew and ﻱﻍﻱﻍﻱﻍ (3030) in Arabic.

As with any Forth, program execution begins with (every) data stack empty and proceeds by reading one word at a time from the source file, parsing it (into root and stem), and executing it.
Data elements are Triliteral words, or the empty word (reading from an empty stack produces the empty word, so DUPing an empty stack is an easy way to produce a zero).
As a general rule, each word operates on the stack designated by its root according to the operation designated by its stem; however there are some important exceptions.

A table of stems follows. Any unused stem is a no-op.

Literals
0 -K-T-B No-op (may be used for commenting)
1 aK-T-B ' push following word to stack (e.g. aKTB B pushes B to stack KTB)
2 uK-T-B " pop n, then push n following words to stack

Stack
4 -KaT-B DUP top stack item
5 aKaT-B DROP top stack item
6 uKaT-B SWAP 1st and 2nd stack items
7 iKaT-B ROT 3rd stack item to top
8 -KuT-B PICK copy nth stack item to top (e.g. Z C T B -> Z C T Z)
9 aKuT-B POKE copy 2nd stack item to nth
10 uKuT-B PUSH pop top of home stack, push to designated stack
11 iKuT-B PULL pop top of designated stack, push to home stack

Arithmetic (integer, saturating)
12 -KiT-B +
13 aKiT-B - (saturating at 0)
14 uKiT-B *
15 iKiT-B / (integer division)

Logical (0 is false, 1 (*a*) is the value of true, but all non-empty words are truthy)
16 -K-TaB > greater than (i.t.o gematria)
17 aK-TaB = equal (in gematria)

Control flow (MARK designates home stack)
18 uK-TaB FORK execute designated stack with home stack, pushing thread id to designated stack
18 iK-TaB JOIN pop designated stack, wait for thread id to finish
20 -KaTaB MARK designate home stack
21 aKaTaB CALL execute designated stack with home stack
22 uKaTaB SKIP n words forwards
23 iKaTaB HOP n words backwards

Text
24 -KuTaB SPLIT top word on stack into letters (ignoring extra vowels)
25 aKuTaB SPLAT first letter of top 6 words on stack into a single word

I/O
26 uKuTaB read a decimal integer (using (Latin) "Arabic" numerals)
27 iKuTaB write a decimal integer
28 -KiTaB READ a word (spaces, punctuation discarded; 0 for EOF)
29 aKiTaB WRITE a word (0 writes a space)
30 uKiTaB read a Unicode character
31 iKiTaB write a Unicode character

In arithmetic, the result word is determined by greedy construction, vowels and consonants alternating.
For example, in Latin script a result of 1024 would be written as *DKQTz*.

For control flow, MARK designates a "home" stack.
For example, the program *eKTB aKTB a KoTB eKTB SaTaK aSTK a aKaTaB* performs the following: first, *aKTB a KoTB* is pushed to stack KTB; then STK is designated the home stack, then *a* is pushed to STK, then KTB is invoked (from the top) with home stack STK, meaning that references to KTB (the called stack) are replaced by STK (the home stack) in the invocation, so *a* is pushed to STK instead of KTB and addition is likewise performed on STK, the result of this program being to push *B* to STK.
