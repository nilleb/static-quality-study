# for every issue in issues_per_file
# obtain the number of issues, the code coverage
# FILE | ISSUES | BUGS | SUPPORT_BUGS | P1 | P2 | P3 | P4 | MAX_COMPLEXITY | COVERAGE | LINES | LINES_COVERED
import json
import os

import lxml.etree as ET
import yaml

step_folder = os.path.dirname(os.path.abspath(__file__))
analysis_parameters = os.path.join(step_folder, "analysis-parameters.yaml")
output_folder = os.path.join(step_folder, "output")
if not os.path.isdir(output_folder):
    if os.path.exists(output_folder):
        os.unlink(output_folder)
    os.mkdir(output_folder)


with open(analysis_parameters) as parameters_file:
    configuration = yaml.load(parameters_file, Loader=yaml.FullLoader)

PROJECT_KEY = configuration["project-key"]

coverage_report = os.path.join(step_folder, configuration.get("coverage-report"))
issues_per_file_path = os.path.join(step_folder, "output/issues_per_file.json",)
bugs_support_path = os.path.join(step_folder, "output/bugs-support.csv")

complexity_report = os.path.join(step_folder, configuration.get("complexity-report"))
hal_report_path = os.path.join(step_folder, configuration.get("hal-report"))

with open(complexity_report) as fp:
    complexity = json.load(fp)

with open(hal_report_path) as fp:
    hal_report = json.load(fp)

with open(issues_per_file_path) as fp:
    issues_per_file = json.load(fp)

bugs_support = {}
bugs_priority = {}
with open(bugs_support_path) as fp:
    for line in fp.readlines():
        if line.startswith(PROJECT_KEY):
            issue_id, is_support, priority = line.split(",")
            is_support = is_support == "True"
            bugs_support[issue_id] = is_support
            bugs_priority[issue_id] = priority.rstrip("\n")

known_bugs = set(bugs_support.keys())
support_bugs = {bug for bug, is_support in bugs_support.items() if is_support}
p1_bugs = {bug for bug, priority in bugs_priority.items() if priority == "P1"}
p2_bugs = {bug for bug, priority in bugs_priority.items() if priority == "P2"}
p3_bugs = {bug for bug, priority in bugs_priority.items() if priority == "P3"}
p4_bugs = {bug for bug, priority in bugs_priority.items() if priority == "P4"}


tree = ET.parse(coverage_report)
xml = tree.getroot()

xpath = "/coverage/packages/package/classes/class"
file_cc_stats = {}
for clazz in xml.xpath(xpath):
    filename = clazz.attrib["filename"]
    line_rate = float(clazz.attrib["line-rate"])
    lines = len(clazz.xpath("lines/line"))
    covered = len(clazz.xpath("lines/line[@hits>0]"))
    file_cc_stats[filename] = (line_rate, lines, covered)


with open(os.path.join(step_folder, "output/jira-cc-statistics.csv"), "w") as fp:
    fp.writelines(
        "FILE,OWNER,ISSUES,BUGS,SUPPORT_BUGS,P1,P2,P3,P4,MAX_COMPLEXITY,COVERAGE,LINES,LINES_COVERED\n"
    )
    for fn, issues in issues_per_file.items():
        line_rate, lines, covered = file_cc_stats.get(fn, (0.0, 0, 0))
        fcomplexity = max(
            item["complexity"] for item in complexity.get(fn, [{"complexity": -1}])
        )
        hal_volume = hal_report.get(fn, {}).get("total")
        hal_volume = hal_volume[7] if hal_volume else -1
        line = (
            '"{filename}",{owner},{issues},{bugs},{support_bugs},'
            "{p1_bugs},{p2_bugs},{p3_bugs},{p4_bugs},"
            "{complexity},{hal_volume},{cc},{lines},{lines_covered}\n"
        ).format(
            filename=fn,
            issues=len(set(issues)),
            bugs=len(set(issues).intersection(known_bugs)),
            support_bugs=len(set(issues).intersection(support_bugs)),
            p1_bugs=len(set(issues).intersection(p1_bugs)),
            p2_bugs=len(set(issues).intersection(p2_bugs)),
            p3_bugs=len(set(issues).intersection(p3_bugs)),
            p4_bugs=len(set(issues).intersection(p4_bugs)),
            complexity=fcomplexity,
            hal_volume=hal_volume,
            cc=line_rate,
            lines=lines,
            lines_covered=covered,
        )
        fp.writelines(line)
