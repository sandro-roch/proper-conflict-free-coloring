# Computing Proper Conflict-Free Colorings #

Given a simple undirected graph $G=(V, E)$, a _proper conflict-free $k$-coloring_ is a coloring, i.e. an assignement $\varphi: V\to\{1, \cdots, k\}$ which is ...

* _proper_, i.e. $\varphi(v)\neq\varphi(w)$ for every pair of adjacent vertices $\{v, w\}\in E$, and ...
* _conflict-free_, i.e. for every non-isolated vertex $v\in V$, there is a color c that is used exactly once among its open neighborhood, $\lvert\{ w\in V: \{v, w\}\in E, \varphi(w)=c \}\rvert = 1$.

This variant of the coloring problem has been investigated, for instance, in (Fabrici, Lužar, Rindošová & Soták, 2023), (Caro, Petruševski, Škrekovski, 2023) and (Cheilaris, 2009). Confligt-free colorings are motivated by the frequency assignment problem: Colors represent different radio frequencies that are assigned to base stations, and the uniqueness property guarantees a frequency that a mobile agent can tune without hearing interference of different base stations; see (Guy et al., 2003). 

This repository provides a simple SAT-implementation that I created while working on specific coloring problems during my PhD. At that time, I was not aware of any other ready-to-use implementation. I hope it may be of use for other researches. I tried to keep the functionality general and extensible; however, I never intended to write a general purpose coloring library and do not claim that my implementation is as efficient as it could be.

## Requirements

All scripts can be executed using Python 3. It requires the package `python-sat` to be installed. For simplicity, I do not provide specific version information.


## Usage

The main file `proper_conflict_free_coloring.py` contains a class ProperConflictFreeColoringSolver` which implements the following methods:

* `__init__(self, G)`
* `find_coloring(number_colors)`
* `enumerate_colorings(number_colors)`
* `count_colorings(number_colors)`
* `conflict_free_chromatic_number()`

The usage should be self-explaining; see also the doc-strings and the test cases.

## License

This project is licensed under the terms of the CC-BY 4.0 license; see `LICENSE.md`.

## References

* Yair Caro, Mirko Petruševski, Riste Škrekovski, _Remarks on proper conflict-free colorings of graphs_, in Disc. Math., vol. 346(2) (2023).
* Panagiotis Cheilaris, Conflict-free coloring, PhD thesis, The City University of New York, 2009.
* Guy Even, Zvi Lotker, Dana Ron, Shakhar Smorodinsky, _Conflict-free colorings of simple geometric regions with applications to frequency assignment in cellular networks_, in SIAM J. Comput., vol. 33(1) (2003).
* Igor Fabrici, Borout Lužar, Simona Rindošová, Roman Soták, _Proper conflict-free and unique-maximum colorings of planar graphs with respect to neighborhoods_, in Disc. Appl. Math., vol. 324 (2023).