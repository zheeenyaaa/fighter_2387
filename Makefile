ifeq ($(OS),Windows_NT)
PYTHON := ./venv/Scripts/python.exe
else
PYTHON := ./venv/bin/python
endif

.PHONY: install run

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m uvicorn main:app --reload
