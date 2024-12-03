from re import findall
from operator import sub

map { findall { r'(\d+)' } | map { int } | list } | transpose
| map { sorted } | transpose | map { (sub | abs ) . splat  }
| sum
