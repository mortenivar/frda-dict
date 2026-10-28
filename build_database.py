#!/usr/bin/env python3

# build_database.py: A script to build a French -> Danish sqlite3 
# dictionary database from a custom text file.
#
# Copyright: Morten Bo Johansen <mortenbo at hotmail dot com>
# Licence: MIT,  https://mit-license.org/
import csv
import re
import sqlite3
import sys
from pathlib import Path

# Files
BASE = Path(__file__).resolve().parent
DICT_FILE = BASE / "french_danish_dictionary.txt"
LEXIQUE_FILE = BASE / "Lexique4.1.tsv"
DATABASE = BASE / "french_danish.db"

# Read Lexique
def load_lexique(filename):
    """
    Returns a dictionary:

        ortho -> phon

    The columns are found by name, so the script does not depend on
    their position in the Lexique file
    """

    pronunciations = {}

    print(f"Reading {filename} ...")

    with open(filename, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")

        if reader.fieldnames is None:
            raise RuntimeError("Lexique file is missing a header.")

        if "ortho" not in reader.fieldnames:
            raise RuntimeError(
                "Could not find the column 'ortho' in the Lexique file."
            )

        if "phon" not in reader.fieldnames:
            raise RuntimeError(
                "Could not find the column 'phon' in the Lexique file."
            )

        for row in reader:
            word = row["ortho"].strip()
            phon = row["phon"].strip()

            if not word or not phon:
                continue

            # Lexique may contain more than one information about the same
            # orthographic form. We use the first non-empty.
            if word not in pronunciations:
                pronunciations[word] = phon

    print(f"  {len(pronunciations):,} different headwords with pronunciations.")

    return pronunciations


# Read french_danish_dictionary.txt
def parse_dictionary(filename, pronunciations):
    """
    Reading french_danish_dictionary.txt, returning entries with:

        headword
        wordclass
        pronunciation
        definition
    """

    entries = []

    unmatched = set()

    pattern = re.compile(r"^(\S+)\s+<([^>]+)>\s*(.*)$")

    print(f"Reading {filename} ...")

    with open(filename, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):

            line = line.strip()

            if not line:
                continue

            match = pattern.match(line)

            if not match:
                print(
                    f"WARNING: Could not parse line "
                    f"{lineno}: {line!r}",
                    file=sys.stderr,
                )
                continue

            headword, wordclass, definitions = match.groups()

            # Find pronunciation.
            pronunciation = pronunciations.get(headword)

            # Try also with minuscules if search does not match directly
            if pronunciation is None:
                pronunciation = pronunciations.get(headword.lower())

            if pronunciation is None:
                unmatched.add(headword)
                pronunciation = ""

            # Semicolon or comma separates definitions.
            defs = [
                d.strip()
                for d in re.split(r"[;,]", definitions)
                if d.strip()
            ]

            if not defs:
                defs = [""]

            for definition in defs:
                entries.append((
                    headword,
                    wordclass,
                    pronunciation,
                    definition,
                ))

    return entries, unmatched


# Create sqlite database
def create_database(filename, entries):

    if DATABASE.exists():
        DATABASE.unlink()

    print(f"Creating {DATABASE} ...")

    con = sqlite3.connect(DATABASE)

    con.executescript("""
        PRAGMA journal_mode = WAL;

        CREATE TABLE dict (
            id             INTEGER PRIMARY KEY,
            headword       TEXT NOT NULL,
            wordclass      TEXT NOT NULL,
            pronunciation  TEXT,
            definition     TEXT NOT NULL
        );

        CREATE INDEX idx_headword
            ON dict(headword);

        CREATE INDEX idx_wordclass
            ON dict(wordclass);
    """)

    con.executemany(
        """
        INSERT INTO dict
            (headword, wordclass, pronunciation, definition)
        VALUES
            (?, ?, ?, ?)
        """,
        entries,
    )

    con.commit()

    # Make database a single, ordiary file
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    con.close()


# Main
def main():

    if not DICT_FILE.exists():
        sys.exit(f"ERROR: {DICT_FILE} not found.")

    if not LEXIQUE_FILE.exists():
        sys.exit(f"ERROR: {LEXIQUE_FILE} not found.")

    pronunciations = load_lexique(LEXIQUE_FILE)

    entries, unmatched = parse_dictionary(
        DICT_FILE,
        pronunciations,
    )

    create_database(DATABASE, entries)

    # Statistics
    con = sqlite3.connect(DATABASE)

    entry_count = con.execute(
        "SELECT COUNT(*) FROM dict"
    ).fetchone()[0]

    word_count = con.execute(
        "SELECT COUNT(DISTINCT headword) FROM dict"
    ).fetchone()[0]

    pronunciation_count = con.execute(
        """
        SELECT COUNT(DISTINCT headword)
        FROM dict
        WHERE pronunciation <> ''
        """
    ).fetchone()[0]

    con.close()

    print()
    print("Færdig.")
    print()
    print(f"  Entries:              {word_count:,}")
    print(f"  Definitions:          {entry_count:,}")
    print(f"  W/pronunciation:      {pronunciation_count:,}")
    print(f"  Wo/pronunciation:     {len(unmatched):,}")
    print()
    print(f"  Database: {DATABASE}")

    if unmatched:
        print()
        print("Headwords without pronunciation in Lexique file:")
        print()

        for word in sorted(unmatched, key=str.lower):
            print(f"  {word}")


if __name__ == "__main__":
    main()
