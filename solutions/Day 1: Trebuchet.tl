from re import findall
from operator import add
map { findall { r'(\d)' } | first add last . phi | int } | sum
