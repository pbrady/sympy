from __future__ import print_function, division

import sys
sys._running_pytest = True
import os

import pytest
from sympy.core.cache import clear_cache
from sympy.external import import_module

# build list of files/modules to ignore during doctests
doctest_ignore = ["doc/src/modules/plotting.rst",  # generates live plots
                  "sympy/utilities/compilef.py",  # needs tcc
                  "sympy/physics/gaussopt.py", # raises deprecation warning
              ]

if import_module('numpy') is None:
    doctest_ignore.extend([
        "sympy/plotting/experimental_lambdify.py",
        "sympy/plotting/plot_implicit.py",
        "examples/advanced/autowrap_integrators.py",
        "examples/advanced/autowrap_ufuncify.py",
        "examples/intermediate/sample.py",
        "examples/intermediate/mplot2d.py",
        "examples/intermediate/mplot3d.py",
        "doc/src/modules/numeric-computation.rst"
    ])

if import_module('matplotlib') is None:
    doctest_ignore.extend([
        "examples/intermediate/mplot2d.py",
        "examples/intermediate/mplot3d.py"
    ])
if import_module('pyglet') is None:
    doctest_ignore.extend(["sympy/plotting/pygletplot"])

if import_module('theano') is None:
    doctest_ignore.extend(["doc/src/modules/numeric-computation.rst"])

def pytest_report_header(config):
    from sympy.utilities.misc import ARCH
    s = "architecture: %s\n" % ARCH
    from sympy.core.cache import USE_CACHE
    s += "cache:        %s\n" % USE_CACHE
    from sympy.core.compatibility import GROUND_TYPES, HAS_GMPY
    version = ''
    if GROUND_TYPES =='gmpy':
        if HAS_GMPY == 1:
            import gmpy
        elif HAS_GMPY == 2:
            import gmpy2 as gmpy
        version = gmpy.version()
    s += "ground types: %s %s\n" % (GROUND_TYPES, version)
    return s


def pytest_terminal_summary(terminalreporter):
    if (terminalreporter.stats.get('error', None) or
            terminalreporter.stats.get('failed', None)):
        terminalreporter.write_sep(
            ' ', 'DO *NOT* COMMIT!', red=True, bold=True)


@pytest.fixture(autouse=True, scope='module')
def file_clear_cache():
    clear_cache()

@pytest.fixture(autouse=True, scope='module')
def check_disabled(request):
    if getattr(request.module, 'disabled', False):
        pytest.skip("test requirements not met.")
    elif getattr(request.module, 'ipython', False):
        # need to check version and options for ipython tests
        if (pytest.__version__ < '2.6.3' and
            pytest.config.getvalue('-s') != 'no'):
            pytest.skip("run py.test with -s or upgrade to newer version.")

def is_doctest(path):
    """ Check if this is a regular '.py' file (indicating doctest). """
    head, tail = os.path.split(path)
    if not tail or tail[-3:] != '.py' or 'tests' in head :
        return False
    return True


ignore_always = ['mpmath', 'benchmark', '__']
def pytest_ignore_collect(path, config):
    """ pytest hook """
    spath = str(path)
    for i in ignore_always:
        if i in spath:
            return True
    if is_doctest(spath):
        for i in doctest_ignore:
            if i in spath:
                return True
