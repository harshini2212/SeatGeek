# BoxOffice — convenience targets.
# On Windows the venv python is .venv/Scripts/python.exe; on POSIX it's .venv/bin/python.
PY ?= python

.PHONY: install demo fraud eval investigate orchestrate serve test clean

install:            ## create venv-less editable install into the active interpreter
	$(PY) -m pip install -e .

demo:               ## full narrated end-to-end showcase
	$(PY) -m boxoffice.cli demo

fraud:              ## fraud metrics, top alerts, detected rings
	$(PY) -m boxoffice.cli fraud

eval:               ## financial-correctness leaderboard (+ per-task detail)
	$(PY) -m boxoffice.cli eval --task-detail

investigate:        ## autonomous investigation of the top alert
	$(PY) -m boxoffice.cli investigate --top

orchestrate:        ## full BoxOffice agent on the top alert
	$(PY) -m boxoffice.cli orchestrate --top

serve:              ## launch the FastAPI service (http://127.0.0.1:8000/docs)
	$(PY) -m boxoffice.cli serve

test:               ## run the offline test suite
	$(PY) -m pytest -q

clean:
	$(PY) -c "import shutil,glob,os; [shutil.rmtree(p,ignore_errors=True) for p in glob.glob('**/__pycache__',recursive=True)+['.pytest_cache','artifacts','data/generated']]"
