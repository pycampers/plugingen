# plugingen

Create `pip` plugins in seconds.

---

For instance, This is how you would go about creating a plugin for the popular package `pipdeptree`:

```python
# pip_plugin_tree.py
import plugingen

cli = plugingen.create(
    code="import pipdeptree\npipdeptree.main()", requirements=["pipdeptree"]
)
```

```python
# setup.py
setup(
    ...
    py_modules=['pip_plugin_tree'],
    entry_points={"console_scripts": ["pip-plugin-tree = pip_plugin_tree:cli"]},
)
```

And that's literally it.

For just this, You get a plugin that automatically gets discovered, works across virtualenvs, without any modification to the original package whatsoever.

```
$ pip tree -l
Django==2.1.4
  - pytz [required: Any, installed: 2018.7]
pip==19.0.dev0
setuptools==40.6.3
wheel==0.32.3
```

---

(This is a prof of concept for a [fork](https://github.com/devxpy/pip) of `pip` that supports plugins.)
