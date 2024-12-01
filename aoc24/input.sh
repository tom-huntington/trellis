#!/usr/bin/sh
set -e
if [ -z "$2" ]
then
    year=$(date '+%Y')
else
    year="$2"
fi
if [ -z "$1" ]
then
    day=$(TZ=':US/Eastern' date '+%-d')
else
    day="$1"
fi
# session_path="$(dirname $0)/session"
# session=$(cat "$session_path")
session=53616c7465645f5fcdd94347ba6c7c1f5be06962f00e0c2f580dd36b33b03665b4ec26f90441bf7892d362dbacd3047483262bedcf92a9821371c5bfe44eb96d
set -x
curl -H "Cookie: session=$session" "https://adventofcode.com/${year}/day/${day}/input" > "d${day}.in"
