component = ./node_modules/component-hooks/node_modules/.bin/component

boot: lib public
	@dev_appserver.py . --port 5000 --admin_port 7000

test: lib
	@python tests.py -f

lib:
	@ln -fs $(PWD)/$@ $@

public: node_modules components
	@$(component) build -n $@ -o $@

node_modules:
	@npm install

components:
	@$(component) install

.PHONY: test boot
