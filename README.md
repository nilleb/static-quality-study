# Correlate bugs

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
