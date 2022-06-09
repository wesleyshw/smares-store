format:
	@black ./app -l 79

check: 
	@black ./app --check

.PHONY: format check