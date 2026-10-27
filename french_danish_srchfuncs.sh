#!/bin/bash

# french_danish_srchfuncs.sh: Some functions to interact with the sqlite3
# database that contains the French -> Danish dictionary.
# Copyright: Morten Bo Johansen <mortenbo at hotmail dot com>
# Licence: MIT,  https://mit-license.org/

DATABASE=${HOME}/.french_danish.db

# MODE=box draws nice (IMO) utf-8 boxes around the search results, but older
# versions of sqlite may have problems with it. And on Termux, they currently
# don't come out well. So here, MODE=list is used by default.
# MODE=list instead.
MODE=list

# French -> Danish dictionary search in sqlite3 database
_frda()
{
  sqlite3 -noheader -cmd ".mode $MODE --limits off" $DATABASE \
  "SELECT headword || ' <' || wordclass || \
  '> /' || pronunciation || '/' || char(10) || \
  group_concat('• ' || definition, char(10)) \
  FROM dict WHERE headword LIKE '$1' COLLATE \
  NOCASE GROUP BY headword, wordclass, pronunciation \
  ORDER BY headword COLLATE NOCASE;"
}

# Danish -> French dictionary search in sqlite3 database (reverse lookup)
_dafr()
{
    sqlite3 -noheader -cmd ".mode $MODE --limits off" "$DATABASE" \
    "SELECT definition || char(10) ||
     group_concat('• ' || headword || ' <' || wordclass || '> ' || '/' ||
     pronunciation || '/', char(10))
     FROM dict
     WHERE ' '||definition||' ' like '% $1 %' COLLATE NOCASE
       AND NOT (definition GLOB '{*}')
     GROUP BY definition, wordclass, pronunciation
     ORDER BY definition COLLATE NOCASE;"
}

# Show all inflexions of French verbs
_fr_infl()
{
    sqlite3 -noheader -cmd ".mode $MODE --limits off" "$DATABASE" \
    "SELECT group_concat('• ' || headword || ' <' || wordclass || '> ' || '/' ||
     pronunciation || '/', char(10)) || char(10) || definition
     FROM dict
     WHERE definition LIKE '%af $1%' COLLATE NOCASE
       AND wordclass = 'v'
     GROUP BY definition, wordclass, pronunciation
     ORDER BY definition COLLATE NOCASE;"
}

# The actual search function
frda()
{
  local prg=_frda
  local srchpat='%%'
  local opt
  local OPTIND=1
  local srchpat_set=false

  while getopts "ria:b:e:h" opt; do
    case $opt in
      r)
        prg=_dafr
        ;;
      i)
        prg=_fr_infl
        ;;
      a)
        srchpat="%${OPTARG}%"
        srchpat_set=true
        ;;
      b)
        srchpat="${OPTARG}%"
        srchpat_set=true
        ;;
      e)
        srchpat="%${OPTARG}"
        srchpat_set=true
        ;;
      h)
        printf '%s\n' \
        'Usage:' \
        '  frda                     print out all entries by French headword' \
        '  frda -r                  print out all entries by Danish headword' \
        '  frda <word>              Danish translation for <word>' \
        '  frda [-r] <word>         French translation for <word> (use dafr instead)' \
        '  frda -a <word>           <word> anywhere' \
        '  frda -b <word>           <word> at beginning' \
        '  frda -e <word>           <word> at end' \
        '  frda -i <verb>           show all inflections of French <verb>' \
        '  frda -h                  show this help'
        return
        ;;
      \?)
        return 1
        ;;
    esac
  done

  shift $((OPTIND - 1))

  if ! $srchpat_set && [[ -n $1 ]]; then
    srchpat="$1"
  fi

  "$prg" "$srchpat"
}

# Danish -> French (reverse lookup)
dafr()
{
  frda -r "$@"
}
