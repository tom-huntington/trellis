from re import findall
from operator import sub
from operator import mul
from collections import Counter
from functools import partial

map { findall { r'(\d+)' } | map { int } | list } | transpose
*| ( ( Counter | partial { index } )  D \ map_f ) N \
map { mul } 
| sum
