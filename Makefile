
DOC_DIR = ./docs

docs:
	$(MAKE) --directory=$(DOC_DIR) html
	firefox $(DOC_DIR)/_build/html/index.html &

clean:
	rm -rf $(DOC_DIR)/_build/html

.PHONY: docs clean
