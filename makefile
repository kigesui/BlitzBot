
init:
	python3 -m pip install -r requirements.txt

test:
	@echo "======================================================================"
	@echo "Running Tests ..."
	@echo "----------------------------------------------------------------------\n"
	python -m unittest discover -s . -p "test_*.py" -v
	@echo "======================================================================"

.PHONY: init test