from re import findall
from itertools import batched
from functools import partial
from operator import mul
from operator import add
from operator import eq
from functools import cmp_to_key

read | split { "\n\n" } *| 
( str.splitlines | partial { in_f } | b [ mul { -2 } | add { 1 } ] | b { str.format { "{}|{}" } }  | cmp_to_key | _reverse_partial { sorted } | s { ( eq ( middle delta \ mul ) . N ) } )
( str.splitlines | map { findall { r'\d+' } | map { int } | list } | list ) 
. Psi { map }
| sum
