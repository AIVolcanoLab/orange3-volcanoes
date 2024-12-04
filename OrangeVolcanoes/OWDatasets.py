import numpy as np
import Thermobar as pt
import pandas as pd

from typing import Optional, Union

from AnyQt.QtCore import Qt

import Orange.data
from Orange.data import Table, ContinuousVariable, StringVariable, Domain
from Orange.widgets.settings import Setting, ContextSetting, DomainContextHandler
from Orange.widgets.utils.itemmodels import DomainModel
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.widget import Input, Output
from orangewidget.widget import Msg
import os
from Orange.data.io import FileFormat

from Orange.data.pandas_compat import table_from_frame,table_to_frame

DATASETS_PATHS = [
    ('Ágreda-López 2024', FileFormat.locate("Ágreda-López_2024-starting_dataset.xlsx",Orange.data.table.dataset_dirs),'xlsx'),
    ('Smith 2021', FileFormat.locate("Smith_glass_post-NYT_1.xlsx",Orange.data.table.dataset_dirs),'xlsx'),
    ('Smith 2021 (Thermobar)', FileFormat.locate("Smith_glass_post-NYT_2.xlsx",Orange.data.table.dataset_dirs),'xlsx')
]


class OWDatasets(OWWidget):
    name = "Datasets"
    description = "Datasets"
    icon = "icons/Datasets.png"
    priority = 1
    keywords = ['Dataset', 'Smith', 'Lopez']

    help = "preprocessing.html"


    GENERIC, FROM_VAR = range(2)

    resizing_enabled = False
    want_main_area = False

    settingsHandler = DomainContextHandler()

    data_type = ContextSetting(GENERIC)

    dataset_idx = Setting(0)

    auto_apply = Setting(True)


    class Outputs:
        data = Output("Data", Table, dynamic=False)


    class Error(OWWidget.Error):
        value_error = Msg("{}")


    def __init__(self):
        OWWidget.__init__(self)

        box = gui.comboBox(self.controlArea, self, "dataset_idx", items=[m[0] for m in DATASETS_PATHS],callback=self._commit)

        self.data_type = DATASETS_PATHS[self.dataset_idx][2]
        self.path = DATASETS_PATHS[self.dataset_idx][1]

        gui.auto_apply(self.buttonsArea, self)


    

    def _commit(self):
        _, self.path, self.data_type = DATASETS_PATHS[self.dataset_idx]
        self.commit.deferred()  


    @gui.deferred
    def commit(self):

        self.clear_messages()

        if self.data_type == 'xlsx':

            df = pd.read_excel(self.path)

        elif self.data_type == 'csv':

            df = pd.read_csv(self.path)

        out = table_from_frame(df)

        self.Outputs.data.send(out)