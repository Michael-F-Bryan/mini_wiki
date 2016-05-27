DOC_DIR = ./docs
package = mini_wiki


# A shell pipeline that'll correctly get the next patch version
next_version = $(shell \
	python3 -c 'import '$(package)'; print('$(package)'.__version__)' | \
	cut -d "+" -f 1 | \
	awk -F "." '{patch = $$3 + 1; print($$1 "." $$2 "." patch) }' )


test:
	py.test

# Alias for test
tests: test

tag:
	@git diff-index --quiet HEAD -- || (printf 'Please commit your changes first.\n\n'; exit 1)
	@echo New version: $(next_version)
	git tag -a "$(next_version)" -m "version $(next_version)"
	git push 
	git push --tags

docs:
	$(MAKE) --directory=$(DOC_DIR) html
	firefox $(DOC_DIR)/_build/html/index.html &

clean:
	rm -rf $(DOC_DIR)/_build/html

coverage:
	coverage run -m pytest
	coverage html
	firefox coverage_report/index.html


.PHONY: docs clean coverage test tag
