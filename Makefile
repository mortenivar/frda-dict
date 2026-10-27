TARGETS = french_danish.db

# Standard handling
all: $(TARGETS)

Lexique4.1.tsv: Lexique4.1.tsv.gz
	gunzip -k Lexique4.1.tsv.gz

french_danish_dictionary.txt: french_danish_dictionary.txt.gz
	gunzip -k french_danish_dictionary.txt.gz

french_danish.db: french_danish_dictionary.txt Lexique4.1.tsv
	@echo "Building French-Danish sqlite3 dictionary database"
	python3 build_database.py

# Install target
install: all
	@echo "Installing sqlite database and shell search functions to $(HOME) ..."
	cp -i french_danish.db $(HOME)/.french_danish.db
	cp -i french_danish_srchfuncs.sh $(HOME)/.french_danish_srchfuncs.sh
	chmod 0644 $(HOME)/.french_danish.db $(HOME)/.french_danish_srchfuncs.sh
	@echo ""
	@echo "Remember to source $(HOME)/.french_danish_srchfuncs.sh"

# Clean target
clean:
	@echo "Cleaning up ..."
	@if [ -e french_danish_dictionary.txt.gz ]; then \
		rm -f french_danish_dictionary.txt; \
	fi
	@if [ -e Lexique4.1.tsv.gz ]; then \
		rm -f Lexique4.1.tsv; \
	fi
	rm -f french_danish.db

.PHONY: all install clean
