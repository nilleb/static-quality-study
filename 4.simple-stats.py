import os
import pandas as pd


relpath = "output/jira-cc-statistics.csv"
path = os.path.abspath(os.path.join(os.path.abspath(''), relpath))

df1 = pd.read_csv(path)

# change the number of quantiles to see the distribution of bugs
NUMBER_OF_QUANTILES = 4

# filter out files other than JS and Python - coverage does not apply to others
# filter out also tests - they usually have high coverage rates
df1 = df1.loc[df1["FILE"].str.endswith("py") | df1["FILE"].str.endswith("js") &~ df1["FILE"].str.contains("tests")]
df1 = df1.loc[df1["FILE"].str.endswith("py") &~ df1["FILE"].str.contains("tests")]

# a short and effective way to display the distribution of bugs
coverage_groupings = df1.groupby(pd.cut(df1.COVERAGE, NUMBER_OF_QUANTILES, include_lowest=True)).sum()
print(coverage_groupings)

pct = 100 / NUMBER_OF_QUANTILES
for left in range(NUMBER_OF_QUANTILES):
    for right in range(left+1, NUMBER_OF_QUANTILES):
        print("The number of bugs in the coverage range {}-{}% is this amount higher than the number of bugs in the coverage range {}-{}%.".format(left*pct, (left+1)*pct, right*pct, (right+1)*pct))
        support_bugs = (coverage_groupings["SUPPORT_BUGS"].iloc[left] / coverage_groupings["SUPPORT_BUGS"].iloc[right] - 1)*100
        print("- support bugs: {:.2f}%".format(support_bugs))
        support_bugs = (coverage_groupings["BUGS"].iloc[left] / coverage_groupings["BUGS"].iloc[right] - 1)*100
        print("- bugs: {:.2f}%".format(support_bugs))

# which are the 10 most complex files?
print(df1.sort_values(by=["COMPLEXITY"], ascending=[False]).head(10))

# top P1 sources
print(df1.sort_values(by=["P1"], ascending=[False]).head(25))

# then, which are the files living in the intersection with at least one P1, one P2 and one P3?
top_buggers2 = df1.loc[(df1.P1 > 0) & (df1.P2 > 0) & (df1.P3 > 0)]
top_buggers2.sort_values(by=["BUGS"], ascending=[False])
