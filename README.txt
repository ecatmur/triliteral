Triliteral (Arabic: <ثلاثي>, Hebrew: <תלת>) is a literate, polyglossal, esoteric, homoiconic, concatenative, self-modifying, Turing-complete language inspired by the *triliteral root* construction common to Semitic languages.
Triliteral programs can be written in the Arabic, Hebrew or (with some loss of fidelity) Latin scripts, though only one at a time; the script used is determined by the file extension: .ثلث, .תלת or .trl.

A Triliteral program is a sequence of *words*, separated by whitespace and/or punctuation, where each word is derived from a (usually tri-)consonantal *root* designating a *variable*, modified by a vowel *stem* designating an *operation*, each consonant having a preceding vowel.
The number of available consonants (and thus the number of variables) depends on the script used, with Triliteral written in Arabic having 25 consonants (hamza not considered a letter) available, Hebrew 18 and Latin 22; in the Semitic scripts these are the letters other than the *matres lectrionis*, whereas in Latin they are the letters other than certain vowels.
The matres lectrionis (full vowels in Latin) are ﺍ, ﻭ and ﻱ in Arabic; א, ה', ו and י in Hebrew, and *aeui* in Latin; however, for the purposes of forming stems, א and ה are considered equivalent, as are a and e in Latin, while the short vowels (which may be designated - entirely optionally - by harakat in Arabic and niqqud in Hebrew, but must be omitted entirely in Latin) are considered together a fourth "vowel"; altogether each script has 4 vowel categories resulting in 4^3 = 64 possible stems.

For purposes of organization the vowels may be considered having the following digit values in a base-4 system: short vowels 0,  ﺍ/א/ה/a/e 1, ﻭ/ו/u 2, and ﻱ/י/i 3, with the *lowest* place value at the *start* of the word (the rightmost position in Arabic and Hebrew, the leftmost in Latin).
For example, the word *aktub* has root KTB and stem a-u, 201 in base 4 (33 in decimal, although this is not used much).
(Note that Triliteral written in the Latin script is case-insensitive, so this could also be written *Aktub*, *aKTuB* etc., with exactly the same meaning.)
Words also have a *numeric* value when used as the object of arithmetic operations, with that value determined (naturally) by *gematria*, adding together the values of the letters (in the common abjadi sequence in Arabic, the Mispar Gadol system in Hebrew, and the Golden Dawn system (*with* digraphs) in Latin) to produce a single value; so, again, *aktub* designates the *number* 1+20+9+6+2 = 38.
Words may have more or fewer than 3 consonants, subject to implementation limits.
Consecutive long vowels are permitted but only the first in each position contribute to the stem; any following contribute only to gematria.
For example, *gematria* is parsed as *-GeMaT(ria)* i.e. root *GMT* and stem *-ea*, where *-* designates an empty position.
The observant will note that this means that any text (for example, this document) can be parsed as a Triliteral program, and that any positive number can be entered; however, Triliteral implementations are required only to support values up to the largest that can be entered with 3 vowels and consonants; for example, *ithithitz* in Latin script (gematria 1630); likewise יציציץ (1110) in Hebrew and ﻱﻍﻱﻍﻱﻍ (3030) in Arabic.

Source is tokenized into words, which occupy a 0-indexed, bounded array.
Data elements are Triliteral words, or the empty word.
Initially, the program counter and all variables are the empty word (i.e. zero).
Program execution proceeds by parsing the word under the program counter into root and stem, incrementing pc, then executing it.
When the program counter reaches the end, execution halts.
Each word operates on the variable designated by its root according to the operation designated by its stem; however there are some important exceptions.

Programs have access to unbounded state in two ways: firstly, every word is of unbounded length, subject to implementation limits, although execution may slow down as increasingly long words are used; secondly, the set of variables is unlimited, again subject to implementation limits, but self-modifying code is necessary to access arbitrary variables.

A table of stems follows. Any unused stem is a no-op.

 0 -K-T-B No-op (may be used for commenting)
 1 aK-T-B ' load following word (e.g. aKTB B loads B to variable KTB)
 2 uK-T-B CLR load empty word
 3 iK-T-B WITH designate first operand for following instruction
 4 -KaT-B LOAD from first operand
 5 aKaT-B STORE to first
 6 uKaT-B SWAP with first
 7 iKaT-B CAT append first (also for addition, logical OR)
 8 -KuT-B SUB first
 9 aKuT-B MUL by first
10 uKuT-B DIV by first
11 iKuT-B MOD by first
12 -KiT-B HOP n words backwards
13 aKiT-B SKIP n words forwards
14 uKiT-B JUMP to address
15 iKiT-B LAND store pc (of next instruction)
16 -K-TaB > greater than (i.t.o gematria)
17 aK-TaB < less than
18 uK-TaB = equal to
19 iK-TaB != not equal to
20 -KaTaB INC
21 aKaTaB DEC
22 uKaTaB NOT (logical: 0 -> 1, all others -> 0)
23 iKaTaB AND (logical)
24 -KuTaB PEEK program memory
25 aKuTaB POKE program memory
26 uKuTaB read a decimal integer (using (Latin) "Arabic" numerals)
27 iKuTaB write a decimal integer
28 -KiTaB READ a word (spaces, punctuation discarded; 0 for EOF)
29 aKiTaB WRITE a word (0 writes a space)
30 uKiTaB read a Unicode character
31 iKiTaB write a Unicode character

2-operand operations take their first operand from the preceding WITH, if any, their second from the variable, and store the result in the variable.
If there is not a preceding WITH, both operands are the variable, so e.g. MUL lets you square a variable in place.

In arithmetic, the result word (other than for CAT) is determined by greedy construction, vowels and consonants alternating.
For example, in Latin script a result of 1024 would be written as *DKQTz*.

For control flow, MARK designates a "home" stack.
For example, the program *eKTB aKTB a KoTB eKTB SaTaK aSTK a aKaTaB* performs the following: first, *aKTB a KoTB* is pushed to stack KTB; then STK is designated the home stack, then *a* is pushed to STK, then KTB is invoked (from the top) with home stack STK, meaning that references to KTB (the called stack) are replaced by STK (the home stack) in the invocation, so *a* is pushed to STK instead of KTB and addition is likewise performed on STK, the result of this program being to push *B* to STK.
