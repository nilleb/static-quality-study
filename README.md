# Software quality study scripts

For a complete study about a monolithic software product being dismissed, please check [STUDY.md](https://github.com/nilleb/ccguard/blob/master/STUDY.md)

## Preliminary information required

### Annotate your code

Please read [Smart commits](https://confluence.atlassian.com/fisheye/using-smart-commits-960155400.html).

### Code coverage report

Please read [this article](https://github.com/nilleb/ccguard/blob/master/docs/how%20to%20produce%20code%20coverage%20data.md).

### The cyclomatic complexity report

#### Python

Please read [this documentation](https://radon.readthedocs.io/en/latest/commandline.html#the-cc-command).

```sh
radon cc src --json --output-file radon.json -i libs -e text_*.py
```

## Procedure

### setup the analysis parameters

### configure the secrets.yaml

### extract information from the software defects database

The script 1-extract-issues-from-jira.py allows the caller to connect to the software defects database and extract all the issues. Two functions (that you can customize) allow you to personalize it. The aim is to produce a CSV on three columns

```csv
Key,IsSupport,Priority
PRJ-8623,True,P2
```

### extract issues from the code commits

Given that your commits have been decorated with the issue they are addressing, like

```txt
fix(PRJ-8623): some bug in production

issue PRJ-8623 blablabla
```

The script 2.extract-issues-from-sources.py extracts the issue Key and the impacted files.
The aim is to produce a json file containing the list of issues for every file

```json
{
    "app/server/my_model.py": [
        "PRJ-8334", "PRJ-5693", "PRJ-4709", "PRJ-2427", "PRJ-5034", "PRJ-5034", "PRJ-4937",
        "PRJ-3728", "PRJ-3712"
    ]
}
```

Only the issues mentioned by the code will be mentioned in the file.

### aggregate code quality and issues

The aim of the script 3-aggregate-coverage-and-issues.py is to produce a report like

```csv
FILE,OWNER,ISSUES,BUGS,SUPPORT_BUGS,P1,P2,P3,P4,COMPLEXITY,HAL_VOLUME,COVERAGE,LINES,LINES_COVERED
"app/server/my_model.py",cms,8,5,4,1,3,1,0,10,450.3799746402741,0.3553,197,70
```

From the different sources of information about the code (coverage, radon-cc, radon-hal, software defects database export).

### simple statistics

Now, let's try to output some statistics about the csv file aggregating all the file-level code quality indicators.
