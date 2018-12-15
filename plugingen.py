import importlib
import json
import os
import sys
from textwrap import dedent
from typing import Set, List

__version__ = "0.0.2"

CODE_TEMPLATE = dedent(
    """
    import sys
    sys.path += {module_dirs}
    sys.argv[1:] = {args}
    {code}
    """
)

PIP_PLUGIN_SCRIPT_PREFIX = "pip-plugin-"


def get_module_dir(module) -> str:
    """Returns the proper package/module directory for `module`"""
    try:
        return os.path.dirname(module.__path__[0])
    except (IndexError, AttributeError):
        return os.path.dirname(module.__file__)


def get_module_dirs(requirements: List[str]) -> Set[str]:
    """Returns the proper package/module directory for all `requirements`"""
    return {get_module_dir(i) for i in map(importlib.import_module, requirements)}


def crash():
    plugin_name = os.path.basename(sys.argv[0])[len(PIP_PLUGIN_SCRIPT_PREFIX) :]
    exit(
        dedent(
            """\
            \033[91m
            Oh no! This is a plugin cli which takes exactly 1 argument, as valid JSON.
            It is only meant to be invoked programatically by \033[96m$ pip\033[91m.
            \033[92m
            You should probably run:

                \033[96m $ pip {0} {1} \033[92m
            
            Instead of:
            
                \033[33m $ pip-plugin-{0} {1} \033[92m                      
            """.format(
                plugin_name, " ".join(sys.argv[1:])
            )
        )
    )


def create(plugin_code: str, requirements: List[str] = []):
    def plugin_cli():
        if len(sys.argv) != 2:
            crash()
        try:
            cmd = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            crash()

        code = CODE_TEMPLATE.format(
            args=cmd["args"],
            module_dirs=get_module_dirs(requirements),
            code=plugin_code,
        )

        os.execve(
            cmd["sys.executable"],
            [cmd["sys.executable"], "-c", code],
            cmd["os.environ"],
        )

    return plugin_cli
