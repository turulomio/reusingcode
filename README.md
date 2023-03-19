# ReusingCode projects
Code that I reuse in several projects

## Reuse files

All files are licensed to GPL-3. So you can reuse them in your projects

To help to include in your prodects you can use github.py module (download_from_github)

For example

```python
self.download_from_github('turulomio','reusingcode','python/connection_pg.py', 'caloriestracker')
```

## Good practices to improve this files

### python

- You should be able to run a file with `python file.py` so add imports with `from casts import x`
- You can

### PyQt5
- You should be able to run a file with `example.py`

## django
- You should add imports with `from .casts.py import x`
