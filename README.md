# Software quality study

## Abstract

Statical analysis of software can give an idea of how distant from the state of art a software is. Code Coverage may be used to assess risk, if it is based over a meaningful set of unit tests. But, are these indicators somehow correlated to the perceived quality of a software? Can these indicators be translated to a number of support issues? Can we use this information to focus our efforts so to improve a software and reduce its Total Cost of Ownership?

## What we know about the topic

In the past years several studies have tried to correlate code coverage with software quality, failing to find a significant correlation. The greatest part of these studies have been conduced on open source software, with a public defects database.

In the case of this study, I have had access to a proprietary software, characterized by its owner as a _monolithic backend_.

## How the data has been collected

We have analyzed the git history of a product being dismantled. For every commit, we have extracted the associated JIRA issues keys and the list of impacted fields. For every file, on the latest available commit, we have extracted the code coverage rate, the number of lines and the covered lines.
We have then extracted from JIRA all the corresponding issues, their kind (Bug), whether they have been reported by the Support, and their priority.

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

## Observation

We observe that the files which have low coverage have the greatest number of bugs, nevermind if they have been found by our teams or our customers.

While the number of issues is not monotonically descending, the number of bugs and support bugs is.

When reducing the analysis to only the files for which we have the LOC information, we see that the total number of lines of code in the lowest code coverage quartile is roughly the half of the number of lines of code in the next quartile: the number of bugs is not proportional to the number of lines.
![code coverage and bugs](https://github.com/nilleb/static-quality-study/raw/master/static/code-coverage-and-number-of-bugs-python-only.png "Distribution of bugs in terms of code coverage")

## Conclusion

A portion of code without code coverage produces the worst software.
A portion of code undergoing a high number of modifications with high coverage is safer than a portion of code with low coverage.
A portion of code with a high coverage does not imply perfect quality.

## Open questions

Bugs cost. Code coverage costs. Which one costs most?
Is there any other static quality indicator to consider in order to determine which files could represent a good investment in terms of code coverage? Good options would be cyclomatic complexity and dependencies analysis (since they translate IMHO in _simpler code can be maintained in a easier way_).
Could be the number of hits in a coverage report used to distinguish good code coverage from bad code coverage?

## References

- [Code Coverage and Postrelease Defects: A Large-Scale Study on Open Source Projects](https://hal.inria.fr/hal-01653728/document)
- [The cost of a bug](https://azevedorafaela.com/2018/04/27/what-is-the-cost-of-a-bug/)
- [Full Stack Python - Code Metrics](https://www.fullstackpython.com/code-metrics.html)
- [Chidamber & Kemerer object-oriented metrics suite](https://www.aivosto.com/project/help/pm-oo-ck.html)
- [Context switches are killing your productivity](https://blog.rescuetime.com/context-switching/)
- [The fallacy of multitasking](https://www.forbes.com/sites/forbestechcouncil/2020/01/31/the-fallacy-of-multitasking/#4807bf5f6ba4)
- [Think Twice Before Using the “Maintainability Index”](https://avandeursen.com/2014/08/29/think-twice-before-using-the-maintainability-index/)
- [The Correlation among Software Complexity Metrics with Case Study](https://arxiv.org/pdf/1408.4523.pdf)
- [Detecting code smells in python](https://www.researchgate.net/publication/311609982_Detecting_Code_Smells_in_Python_Programs)
