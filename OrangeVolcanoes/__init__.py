import Orange.data
import os.path
import os

def get_sample_datasets_dir():
    thispath = os.path.dirname(__file__)
    dataset_dir = os.path.join(thispath, 'datasets')
    return os.path.realpath(dataset_dir)


ICON = 'icons/Volcano.png'

Orange.data.table.dataset_dirs.append(get_sample_datasets_dir())

WIDGET_HELP_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__),'..','docs','build','html'))