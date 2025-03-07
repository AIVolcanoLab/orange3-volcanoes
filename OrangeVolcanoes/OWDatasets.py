import pandas as pd
from Orange.data import Table
from Orange.widgets.settings import Setting, ContextSetting, DomainContextHandler
from Orange.widgets.widget import OWWidget, Output
from Orange.widgets import gui
from orangewidget.widget import Msg
from Orange.data.io import FileFormat
from Orange.data.pandas_compat import table_from_frame
import Orange.data

DATASETS_PATHS = [
    ('Petrelli 2020 Train', FileFormat.locate("Petrelli_et_al_2020__Train_Dataset.xlsx",Orange.data.table.dataset_dirs),'xlsx'),
    ('Petrelli 2020 Test', FileFormat.locate("Petrelli_et_al_2020__Test_Dataset.xlsx",Orange.data.table.dataset_dirs),'xlsx'),
    ('Smith 2011', FileFormat.locate("Smith_et_al_2011.xlsx",Orange.data.table.dataset_dirs),'xlsx'),
    ('Georoc Cpx', FileFormat.locate("Georoc_Cpx_Selected.xlsx",Orange.data.table.dataset_dirs),'xlsx'),
    ('Pawlowsky-Glahn and Egozcue 2006', FileFormat.locate("Pawlowsky-Glahn_and_Egozcue_2006.xlsx",Orange.data.table.dataset_dirs),'xlsx')
]


class OWDatasets(OWWidget):
    name = "Datasets"
    description = "This widget allows users to directly load a set of open-source petrological and volcanological literature datasets into the Orange canvas."
    icon = "icons/Datasets.png"
    priority = 1
    keywords = ['Dataset', 'Smith', 'Lopez']

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