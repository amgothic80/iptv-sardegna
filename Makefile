.PHONY: help run start

help:
	@echo "Comandi disponibili:"
	@echo "  make run      Esegui refresh una volta"
	@echo "  make start    Avvia scheduler (ogni 4 ore)"

run:
	python3 run_cron.py --once

start:
	python3 run_cron.py
