import numpy as np

from typing import Optional, Union

import Orange.data
from Orange.data import Table, ContinuousVariable, StringVariable, Domain
from Orange.widgets.settings import Setting, ContextSetting, DomainContextHandler
from Orange.widgets.utils.itemmodels import DomainModel
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget
from Orange.widgets import gui
from Orange.widgets.widget import Input, Output
from orangewidget.widget import Msg


def alr(x,d):
    x_t = np.log(x/x[d])
    return np.delete(x_t, d)

def geo_mean(x):
    return x.prod()**(1.0/len(x))

def _gram_schmidt_basis(n):
    basis = np.zeros((n, n-1))
    for j in range(n-1):
        i = j + 1
        e = np.array([(1/i)]*i + [-1] +
                     [0]*(n-i-1))*np.sqrt(i/(i+1))
        basis[:, j] = e
    return basis.T

def closure(mat):
    mat = np.atleast_2d(mat)
    if np.any(mat < 0):
        raise ValueError("Cannot have negative proportions")
    if mat.ndim > 2:
        raise ValueError("Input matrix can only have two dimensions or less")
    if np.all(mat == 0, axis=1).sum() > 0:
        raise ValueError("Input matrix cannot have rows with all zeros")
    mat = mat / mat.sum(axis=1, keepdims=True)
    return mat.squeeze()

def clr(x):
    x_t = np.log(x/geo_mean(x))
    return x_t

def ilr(x):
    x = closure(x)
    d = x.shape[-1]
    basis = _gram_schmidt_basis(d)  # dimension (d-1) x d
    return clr(x) @ basis.T


class OWCoDATransformations(OWWidget):
    name = "CoDATransformations"
    description = "Compositional Data Analysis (CoDA) Transformations"
    icon = "icons/CoDATransformations.png"
    priority = 3
    keywords = ['Coda', 'Transformation', 'ilr', 'clr', 'alr']

    INIT_METHODS = (("Alr", alr),
                    ("Clr", clr),
                    ("Ilr", ilr),
                    )

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table, dynamic=False)

    GENERIC, FROM_VAR = range(2)

    resizing_enabled = False
    want_main_area = False

    DEFAULT_PREFIX = "Feature"

    settingsHandler = DomainContextHandler()
    normalization_type = ContextSetting(GENERIC)
    feature_names_column = ContextSetting(None)
    auto_apply = Setting(True)


    class Error(OWWidget.Error):
        value_error = Msg("{}")



    def __init__(self):
        OWWidget.__init__(self)
        self.data = None




        box = gui.radioButtons(
            self.controlArea, self, "normalization_type", box="Transformations",
            callback=self.commit.deferred)

        button = gui.appendRadioButton(box, "centred log ratio transformation (clr)")

        self.meta_button = gui.appendRadioButton(box, "additive log ratio transformation (alr)")
        self.feature_model = DomainModel(
            valid_types=(ContinuousVariable,),
            alphabetical=False)
        self.feature_combo = gui.comboBox(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button)), self,
            "feature_names_column", contentsLength=12, searchable=True,
            callback=self._feature_combo_changed, model=self.feature_model)

        gui.appendRadioButton(box, "isometric log ratio transformation (ilr)")

        gui.auto_apply(self.buttonsArea, self)

    def _apply_editing(self):
        self.normalization_type = self.GENERIC
        #self.feature_name = self.feature_name.strip()
        self.commit.deferred()

    def _feature_combo_changed(self):
        self.normalization_type = self.FROM_VAR
        self.commit.deferred()

    @Inputs.data
    def set_data(self, data):
        # Skip the context if the combo is empty: a context with
        # feature_model == None would then match all domains

        if self.feature_model:
            self.closeContext()
        self.data = data
        self.set_controls()
        if self.feature_model:
            self.openContext(data)
        self.commit.now()

    def set_controls(self):
        self.feature_model.set_domain(Domain(self.data.domain.attributes) if self.data else None)
        self.meta_button.setEnabled(bool(self.feature_model))
        if self.feature_model:
            self.feature_names_column = self.feature_model[0]
        else:
            self.feature_names_column = None

    @gui.deferred
    def commit(self):


        self.clear_messages()

        if self.data is None:
            pass
        elif len(self.data.domain.attributes) > 1:
            if self.normalization_type == 0: #clr

                my_X = np.apply_along_axis(clr, 1, self.data.X)

                print(self.data.domain)
                print(self.data.domain.class_vars)
                print(type(self.data.domain.class_vars))
                print(self.data.domain.metas)


                my_list = [ContinuousVariable(name='clr_'+a.name) for i, a in enumerate(self.data.domain.attributes)]

                my_domain = Domain(my_list, class_vars=self.data.domain.class_vars, metas=self.data.domain.metas)

                transformed = Table.from_numpy(my_domain, my_X, self.data.Y, self.data.metas)

            elif self.normalization_type == 1: #alr

                my_X = np.apply_along_axis(alr, 1, self.data.X, self.data.domain.index(self.feature_names_column))
                
                my_list = [ContinuousVariable(name="log_"+a.name+'_'+self.feature_names_column.name) for i, a in enumerate(self.data.domain.attributes)
                            if i != self.data.domain.index(self.feature_names_column)]

                my_domain = Domain(my_list, class_vars=self.data.domain.class_vars, metas=self.data.domain.metas)
                    

                transformed = Table.from_numpy(my_domain, my_X, self.data.Y, self.data.metas)

            elif self.normalization_type == 2: #ilr
            
                my_X = np.apply_along_axis(ilr, 1, self.data.X)

                my_list = [ContinuousVariable(name="ilr_"+str(a+1))for a in range(my_X.shape[1])]

                my_domain = Domain(my_list, class_vars=self.data.domain.class_vars, metas=self.data.domain.metas)
            
                transformed = Orange.data.Table.from_numpy(my_domain, my_X, self.data.Y, self.data.metas)


        self.Outputs.data.send(transformed)