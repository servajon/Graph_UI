import sys

import numpy as np
import scipy.signal
from PyQt5.QtCore import QObject, pyqtSignal
from joblib.numpy_pickle_utils import xrange
from lmfit.models import GaussianModel, VoigtModel, PseudoVoigtModel
from scipy import sparse
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as pplot

from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure


def get_index(array, value):
    index = 0
    while array[index] <= value:
        index += 1
    return index


def get_index_pics(pics):
    _max = 0
    _min = sys.maxsize
    for pic in pics:
        _min = min(_min, pic.index_min)
        _max = max(_max, pic.index_max)
    return _min, _max


def baseline_als(y, lam, p, niter=5):
    L = len(y)
    D = sparse.csc_matrix(np.diff(np.eye(L), 2))
    w = np.ones(L)
    for i in xrange(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z


def fit_pics(_x_array, _y_array, pics):
    param = None
    fits = {}

    index_min, index_max = get_index_pics(pics)

    x_array = _x_array[index_min:index_max]
    y_array = _y_array[index_min:index_max]

    """pplot.plot(x_array, y_array)"""
    baseline = baseline_als(y_array, 10000, 0.0001)

    """pplot.plot(x_array, baseline)"""

    y_array -= baseline

    x_array = np.array(x_array)
    y_array = np.array(y_array)

    for i, pic in enumerate(pics):
        if pic.fit == "_GaussianModel":
            name = "pic" + str(i) + pic.fit
            model = GaussianModel(prefix=name + "_")
        elif pic.fit == "_VoigtModel":
            name = "pic" + str(i) + pic.fit
            model = VoigtModel(prefix=name + "_")
        elif pic.fit == "_PseudoVoigtModel":
            name = "pic" + str(i) + pic.fit
            model = PseudoVoigtModel(prefix=name + "_")
        else:
            raise ValueError

        if param is None:
            param = model.make_params()
        else:
            param.update(model.make_params())

        param[name + "_center"].set(pic.x_max)
        param[name + "_amplitude"].set(pic.integral)
        param[name + "_sigma"].set(pic.fwhm)

        fits[name] = model

    mod = None
    for value in fits.values():
        if mod is None:
            mod = value
        else:
            mod += value

    out = mod.fit(y_array, param, x=x_array)

    for i, pic in enumerate(pics):
        key = "pic" + str(i) + pic.fit
        pic.x_max = out.values[key + "_center"]
        pic.integral = out.values[key + "_amplitude"]
        pic.fwhm = out.values[key + "_fwhm"]

        pic.index_min = get_index(_x_array, pic.x_max - pic.fwhm * 2 * 1.5)
        pic.index_max = get_index(_x_array, pic.x_max + pic.fwhm * 2 * 1.5)

    """pplot.plot(x_array, y_array)
    pplot.plot(x_array, out.best_fit)
    pplot.show()"""


def VoigtModel_fit(x_array, y_array, name, pic):
    baseline = baseline_als(y_array, 10000, 0.0001)
    y_array -= baseline

    # y_array = scipy.signal.savgol_filter(y_array, 21, 7)

    name += "_VoigtModel"
    voigt = VoigtModel(prefix=name + '_')

    pars = voigt.make_params()

    pars[name + "_center"].set(pic.x_max)
    pars[name + "_amplitude"].set(pic.integral)
    pars[name + "_sigma"].set(pic.fwhm)

    out = voigt.fit(y_array, pars, x=x_array)

    """pplot.plot(x_array, y_array)
    pplot.plot(x_array, out.best_fit)
    pplot.show()"""

    return out


def PseudoVoigtModel_fit(x_array, y_array, name, pic):
    baseline = baseline_als(y_array, 10000, 0.0001)
    y_array -= baseline

    # y_array = scipy.signal.savgol_filter(y_array, 21, 7)

    name += "_PseudoVoigtModel"
    pseudoVoigt = PseudoVoigtModel(prefix=name + '_')

    pars = pseudoVoigt.make_params()

    pars[name + "_center"].set(pic.x_max)
    pars[name + "_amplitude"].set(pic.integral)
    pars[name + "_sigma"].set(pic.fwhm)

    out = pseudoVoigt.fit(y_array, pars, x=x_array)

    """pplot.plot(x_array, y_array)
    pplot.plot(x_array, out.best_fit)
    pplot.show()"""

    return out


def GaussianModel_fit(x_array, y_array, name, pic):
    baseline = baseline_als(y_array, 10000, 0.0001)
    y_array -= baseline

    # y_array = scipy.signal.savgol_filter(y_array, 21, 7)

    name += "_GaussianModel"
    gaussian = GaussianModel(prefix=name + '_')

    pars = gaussian.make_params()

    pars[name + "_center"].set(pic.x_max)
    pars[name + "_amplitude"].set(pic.integral)
    pars[name + "_sigma"].set(pic.fwhm)

    out = gaussian.fit(y_array, pars, x=x_array)

    """pplot.plot(x_array, y_array)
    pplot.plot(x_array, out.best_fit)
    pplot.show()"""

    return out


def get_delta_centre_moyen(past_param):
    if len(past_param) < 2:
        return None
    else:
        s = 0
        for i in range(1, len(past_param)):
            s += abs(past_param[i - 1][0] - past_param[i][0])
        return s / (len(past_param) - 1)


class Fitting(QObject):
    finished = pyqtSignal(int)

    def __init__(self, figure, pics):
        QObject.__init__(self)

        self.figure = figure
        self.new_figure = None

        x_datas = []
        y_datas = []
        for i in range(len(self.figure.x_axe.data)):
            x_datas.append(self.figure.x_axe.data[i].data)
            y_datas.append(self.figure.y1_axe.data[i].data)

        self.x_datas = x_datas
        self.y_datas = y_datas

        self.pics = []
        self.create_pic(pics)

        self.center = []
        self.area = []
        self.fwhm = []

        index_min, index_max = get_index_pics(self.pics)
        self.init_index_min = index_min
        self.init_index_max = index_max

        self.init_center = [pic.x_max for pic in self.pics]

    def create_pic(self, pics):
        for pic in pics:
            self.pics.append(Pic(pic[2], pic[3], pic[4], pic[0], pic[1]))

    def run(self):
        # on regarde le meilleur fit pour chaque fit
        for pic in self.pics:
            self.best_fit(pic)

        for pic in self.pics:
            print(pic.fit)

        # on fit tous les pics
        for i in range(len(self.x_datas)):
            print("cycle " + str(i))
            fit_pics(self.x_datas[i], self.y_datas[i], self.pics)
            center = []
            area = []
            fwhm = []
            for pic in self.pics:
                center.append(pic.x_max)
                area.append(pic.integral)
                fwhm.append(pic.fwhm)
            self.center.append(center)
            self.area.append(area)
            self.fwhm.append(fwhm)

        self.finished.emit(1)


    def best_fit(self, pic):
        x_array = pic.slice(self.x_datas[0])
        y_array = pic.slice(self.y_datas[0])

        result_gauss = GaussianModel_fit(x_array, y_array, "cycle0", pic)
        result_voigt = VoigtModel_fit(x_array, y_array, "cycle0", pic)
        result_pseudovoigt = PseudoVoigtModel_fit(x_array, y_array, "cycle0", pic)

        sum_gauss = 0
        sum_voigt = 0
        sum_pseudovoigt = 0
        for param in result_gauss.params:
            sum_gauss += result_gauss.params[param].stderr / result_gauss.params[param].value

        for param in result_voigt.params:
            if not "_gamma" in param:
                sum_voigt += result_voigt.params[param].stderr / result_voigt.params[param].value

        for param in result_pseudovoigt.params:
            if not "_fraction" in param:
                sum_pseudovoigt += result_pseudovoigt.params[param].stderr / result_pseudovoigt.params[param].value

        _min = min(sum_gauss, sum_voigt, sum_pseudovoigt)
        if _min == sum_gauss:
            pic.fit = "_GaussianModel"
        elif _min == sum_voigt:
            pic.fit = "_VoigtModel"
        else:
            pic.fit = "_PseudoVoigtModel"


class Pic:
    def __init__(self, x_max, integral, fwhm, index_min, index_max):
        self.x_max = x_max
        self.integral = integral
        self.fwhm = fwhm

        self.index_min = index_min
        self.index_max = index_max

        self.fit = None

    def update(self, x_max, integral, fwhm):
        self.x_max = x_max
        self.integral = integral
        self.fwhm = fwhm

    def slice(self, array):
        return array[self.index_min:self.index_max]

    def __repr__(self):
        return "x_max : " + str(self.x_max) + "\n" + "integral : " + str(self.integral) + "\n" + "fwhm : " + str(
            self.fwhm)


if __name__ == '__main__':
    x_arrays = []
    y_arrays = []

    file = open(r"C:\Users\Maxime\Desktop\export_diffraction.txt", "r")

    data = file.readlines()

    index = 0
    while index < len(data):
        line = data[index].split("\t")
        line[-1] = line[-1][-1]
        for i in range(len(line) - 1):
            line[i] = float(line[i])
        x_arrays.append(line[:-1])

        index += 1

        line = data[index].split("\t")
        line[-1] = line[-1][-1]
        for i in range(len(line) - 1):
            line[i] = float(line[i])
        y_arrays.append(line[:-1])

        index += 1

    p1 = [3886, 3927, 23.8239, 2843.3179328999577, 0.01351489612034243]
    p2 = [3938, 3979, 24.0999, 3684.581274899939, 0.03926934953668848]

    pics = [p1, p2]
    fitting = Fitting(x_arrays, y_arrays, pics)
    fitting.run()







