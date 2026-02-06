VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
GOLDEN := tests/fixtures/golden

.PHONY: help venv install install-dev test update-golden clean

help:
	@echo "make venv           - create virtualenv"
	@echo "make install        - install runtime deps"
	@echo "make install-dev    - install runtime + test deps"
	@echo "make test           - run pytest"
	@echo "make update-golden  - regenerate golden JSON from XML (review diff before committing)"
	@echo "make clean          - remove venv and build artifacts"

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

venv: $(VENV)/bin/activate

install: venv
	$(PIP) install -r requirements.txt

install-dev: venv
	$(PIP) install -r requirements-dev.txt

test: install-dev
	$(PYTEST) tests/ -v

update-golden: install
	@echo "regenerating golden JSON files — review the diff before committing"
	$(PYTHON) -c "\
import json, xmltodict; \
from blog_to_json import wordpress_xml_dict_to_normalized_dict as wp, disqus_xml_dict_to_normalized_dict as dq; \
pairs = [ \
    ('$(GOLDEN)/russellballestrini.wordpress.2017-09-05.xml', '$(GOLDEN)/russellballestrini.wordpress.json', wp), \
    ('$(GOLDEN)/printableprompts.WordPress.2022-05-18.xml', '$(GOLDEN)/printableprompts.json', wp), \
    ('$(GOLDEN)/wingitmom.WordPress.2022-05-18.xml', '$(GOLDEN)/wingitmom.com.json', wp), \
    ('$(GOLDEN)/brettterpstra-2019-03-01T21_42_06.627201-all.xml', '$(GOLDEN)/brettterpstra.json', dq), \
]; \
[open(j,'w').write(json.dumps(fn(xmltodict.parse(open(x).read())), indent=2)) or print(f'  wrote {j}') for x,j,fn in pairs]"
	@echo "done — now run: git diff $(GOLDEN)/*.json"

clean:
	rm -rf $(VENV) build dist *.egg-info .eggs __pycache__
