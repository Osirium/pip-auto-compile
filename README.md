# pip-auto-compile

A [Pre-Commit](https://pre-commit.com) hook to compile modified requirements.in files into requirements.txt files.
Works with both Python2, and Python3, so you can regenerate requirements.txt
with the correct interpreter version, just specify `language_version` in your pre-commit hooks config.

# Usage

```yaml
- repo: https://github.com/samathy/pip-auto-compile
    rev: 0.1.0
    hooks:
        - id: pip-auto-compile
          files: requirements(-[^.*])?in$
          language: python
          language_version: python3  
        - id: pip-auto-compile
          files: python_2_src/requirements(-[^.*])?in$
          language: python
          language_version: python2.7
          args:
          - --pip-compile-arg=--allow-unsafe
```


