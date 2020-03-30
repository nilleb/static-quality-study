import json
import fnmatch
import re
from collections import defaultdict
from pathlib import Path

import os
import git
import yaml

step_folder = os.path.dirname(os.path.abspath(__file__))
analysis_parameters = os.path.join(step_folder, "analysis-parameters.yaml")
output_folder = os.path.join(step_folder, "output")
if not os.path.isdir(output_folder):
    if os.path.exists(output_folder):
        os.unlink(output_folder)
    os.mkdir(output_folder)

issues_per_file_path = os.path.join(output_folder, "issues_per_file.json")
files_per_jira_issue_path = os.path.join(output_folder, "files_per_jira_issue.json")
print("The output files will be:\n- {}\n- {}".format(issues_per_file_path, files_per_jira_issue_path))


with open(analysis_parameters) as parameters_file:
    configuration = yaml.load(parameters_file, Loader=yaml.FullLoader)

REPO_FOLDER = configuration["repo-folder"]
PROJECT_KEY = configuration["project-key"]
LIMIT = configuration["git-history-limit"]
STOP_AFTER_THIS_NUMBER_OF_COMMITS_WITHOUT_ISSUES = configuration[
    "stop-after-this-number-of-commits-without-issues"
]


def filter_paths(paths):
    inclusions = configuration["files-selection"]["include"]
    exclusions = configuration["files-selection"]["exclude"]
    for path in paths:
        include = False
        for inclusion in inclusions:
            include |= fnmatch.fnmatch(path, inclusion)
        for exclusion in exclusions:
            include &= not fnmatch.fnmatch(path, exclusion)
        if include:
            yield path


def compute_jira_file_statistics(
    project_key, repo_folder=".", limit=-1, stop_after=1000
):
    repo = git.Repo(repo_folder, search_parent_directories=True)

    issue_key_regex = re.compile("{}-[0-9]+".format(project_key))

    def jira_key(message):
        return issue_key_regex.findall(message, re.MULTILINE)

    files_per_jira_issue = {}
    issues_per_file = defaultdict(list)

    last_commits_had_an_issue = []
    for logEntry in list(repo.iter_commits())[:limit]:
        commit = repo.commit(logEntry)
        paths = list(filter_paths(commit.stats.files.keys()))
        commit_title = commit.message.split("\n")[0]
        keys = jira_key(commit.message)
        #print(
        #    "commit {} ({}), issues {}: {} files".format(
        #        commit.hexsha[:7], commit_title, keys, len(paths)
        #    )
        #)
        for key in keys:
            files_per_jira_issue[key] = paths
            for path in paths:
                issues_per_file[path].append(key)

        last_commits_had_an_issue.append(len(keys) > 0)

        if len(last_commits_had_an_issue) > stop_after and all(
            last_commits_had_an_issue[-stop_after:]
        ):
            print(
                "Stopping because I can not find more jira issues.",
                len(last_commits_had_an_issue),
            )
            break

    print("Processed %d commits.", len(last_commits_had_an_issue))

    return files_per_jira_issue, issues_per_file


files_per_jira_issue, issues_per_file = compute_jira_file_statistics(
    PROJECT_KEY, REPO_FOLDER, LIMIT, STOP_AFTER_THIS_NUMBER_OF_COMMITS_WITHOUT_ISSUES,
)


with open(issues_per_file_path, "w") as fp:
    json.dump(issues_per_file, fp)

with open(files_per_jira_issue_path, "w") as fp:
    json.dump(files_per_jira_issue, fp)
