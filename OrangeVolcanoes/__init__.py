import sysconfig

import Orange.data
import os.path
import os

def get_sample_datasets_dir():
    thispath = os.path.dirname(__file__)
    dataset_dir = os.path.join(thispath, 'datasets')
    return os.path.realpath(dataset_dir)


ICON = 'icons/Volcano.png'

Orange.data.table.dataset_dirs.append(get_sample_datasets_dir())

WIDGET_HELP_PATH = (
    # Development documentation (in editable mode)
    # You need to build help pages manually using
    # make html
    # inside docs/ folder
    ("{DEVELOP_ROOT}/docs/build/html/index.html", None),

    # Documentation included in wheel
    # Correct DATA_FILES entry is needed in setup.py and documentation has to be built
    # before the wheel is created.
    ("{}/help/orange3-volcanoes/index.html".format(sysconfig.get_path("data")), None),

    # Online documentation url, used when the local documentation is available.
    # Url should point to a page with a section Widgets. This section should
    # include links to documentation pages of each widget. Matching is
    # performed by comparing link caption to widget name.
    ("https://orange3-volcanoes.readthedocs.io/en/latest/", ""),
)


