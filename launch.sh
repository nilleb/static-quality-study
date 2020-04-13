# before executing this script, make sure you have edited analysis-parameters.xml
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python3 1-extract-issues-from-jira.py
python3 2-extract-issues-from-sources.py
python3 3-aggregate-coverage-and-issues.py
# at this point you obtain a CSV output/jira-cc-statistics.csv
