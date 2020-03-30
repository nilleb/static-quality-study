import logging
import os

import yaml
from jira import JIRA

step_folder = os.path.dirname(os.path.abspath(__file__))
analysis_parameters = os.path.join(step_folder, "analysis-parameters.yaml")
secrets_path = os.path.join(step_folder, "secrets.yaml")
output_folder = os.path.join(step_folder, "output")
if not os.path.isdir(output_folder):
    if os.path.exists(output_folder):
        os.unlink(output_folder)
    os.mkdir(output_folder)

bugs_support_path = os.path.join(output_folder, "bugs-support.csv")

with open(analysis_parameters) as parameters_file:
    configuration = yaml.load(parameters_file, Loader=yaml.FullLoader)

with open(secrets_path) as secrets_file:
    secrets = yaml.load(secrets_file, Loader=yaml.FullLoader)

jira_url = configuration["jira"]
jc = secrets["jira"][jira_url]

client = JIRA(jira_url, basic_auth=(jc["user"], jc["token"]))

PROJECT_KEY = configuration["project-key"]


def an_adequate_jql_generator():
    """
    Please provide in this function a JQL expression that extracts your bugs from jira
    """
    return 'type = "Bug" and project={}'.format(PROJECT_KEY)


def is_support_issue(issue):
    """
    Please provide an euristic to determine whether the issue is a production one
    (ie. it has been collected by the support)
    """
    return "support" in issue.fields.labels


jql = an_adequate_jql_generator()

with open(bugs_support_path, "w") as fp:
    fp.writelines("Key,IsSupport,Priority\n")
    block_size = 100
    block_num = 0
    while True:
        start_idx = block_num * block_size
        issues = client.search_issues(jql, start_idx, block_size)
        if len(issues) == 0:
            break
        block_num += 1
        for issue in issues:
            logging.info("%s: %s" % (issue.key, issue.fields.summary))
            fp.writelines(
                "{key},{is_support},{priority}\n".format(
                    key=issue.key,
                    is_support=is_support_issue(issue),
                    priority=issue.fields.priority.name,
                )
            )
