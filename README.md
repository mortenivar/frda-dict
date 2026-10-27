# French->Danish dictionary with reverse lookup function for Danish->French

## Files in This Repository:

This repository contains the following files:
- **french_danish_dictionary.txt.gz** - a compressed, raw text file with a French->Danish dictionary.
- **build_database.py** - a python script to build an sqlite3 dictionary database from the text file.
- **french_danish_srchfuncs.sh** - a bash script which provides the user search functions.
- **Lexique4.1.tsv.gz** - a compressed tab separated text file, holding phonetic information for about 170.000 French words
- **Makefile** - a make(1) script to automate building and installing the dictionary.

---

## Prerequisites

Currently, only unix-like systems like Linux are supported, but since both
python and sqlite3 should be fairly platform agnostic, then making it work
on Windows shouldn't be too hard, I suppose; probably only the bash script
and the Makefile need to be converted to Windows batch files. If you know
how to do that and are able to test it, you're welcome to send me the files
and I'll include them.

---

## Features
- **About 200.000 French headwords**. This includes inflected forms of French verbs.
- **About 25.000 French headwords with Danish translations**. Translations for each headword may be multiple.
- **About 54.000 Danish->French translations**. This is provided with the reverse lookup function.
- **Pronunciation (IPA):** Features native French phonetic pronunciation (from Lexique).

---


## Compilation and Building (Linux)

### 1. Compile the Dictionaries
To unpack the source text and phonetics files and execute the Python compilation script, simply run:
```bash
make
```
This will automatically generate the required sqlite3 database file, **french_danish.db**

---

## Installation (Linux)

### 2. Install the Database File and the Bash Script 
```bash
make install
```
This will install the files, french_danish.db and french_danish_srchfuncs.sh\
to $HOME/.french_danish_srchfuncs.sh and $HOME/.french_danish.db, i.e. as
hidden files in your home directory.

After this, you must make the search functions available in your terminal.\
In your $HOME/.bashrc or similar, insert the lines

```bash
if [[ -r ~/.french_danish_srchfuncs.sh ]]; then
. ~/.french_danish_srchfuncs.sh
fi
```
and restart the terminal (or source the file).

### 3. Clean Up Temporary Files
To remove the compiled dictionary file and the unpacked text dictionary and phonetics files, run:
```bash
make clean
```
---

## Usage

Everything is terminal based, so in your favourite terminal first do:

**Show Help:**
```bash
frda -h

Usage:
  frda                     print out all entries by French headword
  frda -r                  print out all entries by Danish headword
  frda <word>              Danish translation for <word>
  frda [-r] <word>         French translation for <word> (use dafr instead)
  frda -a <word>           <word> anywhere
  frda -b <word>           <word> at beginning
  frda -e <word>           <word> at end
  frda -i <verb>           show all inflections of French <verb>
  frda -h                  show this help
```

So, the main command is "frda", with options to have the search expression
form the beginning or end of possible matches as well as matching anywhere.

The command

```bash
frda -i être
```
Will print out all 44(!) inflections of the French verb for "to be".

---

**French to Danish:**
```bash
frda hibou
```
*Output example:*
> hibou <m, h aspiré> /ibu/
> - ugle
> - hornugle
> - enspænder

showing that the French word for 'owl' is a noun of gender masculine and
that the 'h' is aspirated. Then, it shows the phonetic representation of the
word's pronunciation between the two slashes. Finally, it shows three
possible Danish translations of the word. On my system, Arch Linux, using
sqlite3, version 3.54.0, the output will be shown with a nice utf-8 box
around it by default, but the boxed output format may create problems on
Termux and with older versions of sqlite, so I have made the output format
default to 'list'. You may want to edit the french_danish_srchfuncs.sh script
at around line 14 and change the line

MODE=list to MODE=box

and see how it goes.

Otherwise, see the Wikipedia page [French phonology](https://en.wikipedia.org/wiki/French_phonology) for an
explanation of the phonetic symbols.

Since the command
```bash
frda
```
with no options, spews out all the entries in the dictionary, you may use
that to create more fine-grained searches with 'grep' or 'awk'.

---

**Danish to French:**

The command
```bash
frda -r <word>
```
will perform a reverse lookup for word, thereby doing a translation from
Danish to French. However, a convenience function 'dafr' is provided which
takes the same arguments a 'frda'. So the command
```bash
dafr ugle
```
*Output example:*
> ugle
> - chouette <f> /ʃwɛt/
> ugle
> - hibou <m, h aspiré> /ibu/\
> ugle (ens) hår
> - décoiffer <v> /dekwafe/

shows the French translations of the Danish word 'ugle ('owl'), revealing that
'ugle' can be both 'hibou' and 'chouette' and also that it is a verb, meaning
to ruffle one's hair.

---

## Using the Dictionary on an Android Phone with Termux

The dictionary works out of the box on the Android terminal emulator,
Termux. To install it to your phone, do the following:

In Termux
```bash
pkg update
pkg install git python sqlite make nano
mkdir src
cd src
git clone https://github.com/mortenivar/frda-dict.git
cd frda-dict
make
make install
cd
```
Remember to source the bash script as per above. You may edit the .bashrc
file in the Termux home directory with nano.

On an iPhone, maybe iSH will also work?

---

## Contributing

Translations of new words are always welcome. If you have any you would like to share, I
prefer that you send them to me at \<mortenbo at hotmail dot com\>

---
## Attributions, Copyrights & Licenses

This project is a data compilation (a derivative work) merging several
independent academic and open-source linguistic resources. The individual
source licenses are fully compatible with this aggregation and are
distributed under the following terms:

### 1. French Inflected Forms, Inria LEFF (Lexique des Formes Fléchies du Français, developed by Inria)
- **Source:** Source file archived at: [lefff-3.4](https://web.archive.org/web/20200420151411if_/https://gforge.inria.fr/frs/download.php/file/34600/lefff-3.4.tar.gz)
- **Copyright:** INRIA 2007
- **License:** **LGPLLR** (Lesser General Public License For Linguistic Resources).
- **Terms:** Permits free redistribution and integration as a linguistic component within third-party applications and databases without enforcing its own copyleft restrictions on the broader project.

### 2. French Phonetics and Pronunciation (Lexique.org)
- **Source:** [Lexique.org](http://lexique.org) developed by Christophe Pallier, Boris New, Jessica Bourgin and Mathias Sablé-Meyer (OpenLexicon project).
- **License:** **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.
- **Terms:** The phonetic transcription data has been included and paired in compliance with the NonCommercial provisions. Any redistribution of the French phonetic dataset requires proper attribution to the original authors.
  
### 3. French to Danish translations
This applies to the file:

**french_danish_dictionary.txt**

- **Source:** Various, including Larousse.
- **Copyright:** Morten Bo Johansen <mortenbo at hotmail dot com>
- **License:** **LGPLLR** (Lesser General Public License For Linguistic Resources).

### 4. Project Utility Scripts
This applies to the files:

**build_database.py**\
**french_danish_srchfuncs.sh**\
**Makefile**

- **Copyright:** Morten Bo Johansen \<mortenbo at hotmail dot com\>
- **License:** [**MIT**](https://mit-license.org/)
