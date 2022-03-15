import math
import sys

import numpy as np
import scipy.signal
from PyQt5.QtCore import QObject, pyqtSignal
from joblib.numpy_pickle_utils import xrange
from lmfit.models import GaussianModel, VoigtModel, PseudoVoigtModel
from scipy import sparse
from scipy.sparse.linalg import spsolve
from derivative import dxdt
import matplotlib.pyplot as pplot

from Console_Objets.Data_array import Data_array
from Console_Objets.Figure import Figure


def get_index(array, value):
    index = 0
    while array[index] <= value:
        index += 1
    return index


def slice(array_x, array_y, v1, v2):
    index = 0
    while array_x[index] < v1:
        index += 1
    index_min = index
    while array_x[index] < v2:
        index += 1
    return array_x[index_min:index + 1], array_y[index_min:index + 1]


def get_min_max_pics(pics):
    _max = 0
    _min = sys.maxsize
    for pic in pics:
        _min = min(_min, pic.left_base)
        _max = max(_max, pic.right_base)
    return _min, _max


def baseline_(y, lam, p, niter=5):
    L = len(y)
    D = sparse.csc_matrix(np.diff(np.eye(L), 2))
    w = np.ones(L)
    for i in xrange(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z


def pseudo_voigt(x, amplitude, center, sigma, fraction):
    sigma_g = sigma / math.sqrt(2 * math.log(2))
    return ((1 - fraction) * gaussian(x, amplitude, center, sigma_g) +
            fraction * lorentzian(x, amplitude, center, sigma))


def gaussian(x, amplitude=1.0, center=0.0, sigma=1.0):
    return ((amplitude/(max(1.0e-15, math.sqrt(2*math.pi)*sigma)))
            * math.e ** (-(1.0*x-center)**2 / max(1.0e-15, (2*sigma**2))))


def lorentzian(x, amplitude=1.0, center=0.0, sigma=1.0):
    return ((amplitude/(1 + ((1.0*x-center)/max(1.0e-15, sigma))**2))
            / max(1.0e-15, (math.pi*sigma)))


def delimit_pic(x, y, center):
    index = 0
    while x[index] < center:
        index += 1

    index_center = index

    while index - 1 > -1 and y[index - 1] < y[index]:
        index -= 1

    if index_center - index < 3:
        raise ValueError

    val_min = x[index]

    index = index_center

    while index + 1 < len(y) and y[index + 1] < y[index]:
        index += 1

    if index - index_center < 3:
        raise ValueError

    val_max = x[index]

    return val_min, val_max




def fit_pics(_x_array, _y_array, pics, nb):

    _min, _max = get_min_max_pics(pics)
    x_array, y_array = slice(_x_array, _y_array, _min * 0.99, _max * 1.01)

    y_array = scipy.signal.savgol_filter(y_array, 5, 3)

    baseline = baseline_(y_array, 10000, 0.0001)

    y_array -= baseline



    for pic in pics:

        """try:
            left_base, right_base = delimit_pic(x_array, y_array, pic.center)
            pic.left_base = left_base
            pic.right_base = right_base
        except (ValueError, IndexError):
            pass"""



        pplot.plot(x_array, y_array)
        temp_x, temp_y = slice(x_array, y_array, pic.left_base, pic.right_base)

        pplot.plot(temp_x, temp_y)
        """temp_x = x_array
        temp_y = y_array"""

        """pplot.plot(temp_x, temp_y)
        pplot.show()"""


        model = PseudoVoigtModel()

        param = model.make_params()

        for key, item in pic.__dict__.items():
            if key != "left_base" and key != "right_base" and key != "fit":
                param[key].set(value=item)

        # param["amplitude"].set(value=pic.amplitude)
        # param["sigma"].set(value=pic.fwhm)

        out = model.fit(temp_y, param, x=temp_x)

        print('------------------')
        print(out.values)



        # pic.update(**out.values)



        # pplot.plot(x_array, y_array)
        # pplot.plot(temp_x, out.best_fit)

        """def pseudo_voigt(x, amplitude, center, sigma, fraction):"""

        test_voigt = pseudo_voigt(np.array(x_array), out.values["amplitude"], out.values["center"], out.values["sigma"],
                                  out.values["fraction"])

        # left_base, right_base = out_fit_min_max(x_array, test_voigt, out.values["center"])
        # pic.left_base = pic.center - 1.8 * pic.fwhm
        # pic.right_base = pic.center + 1.8 * pic.fwhm

        pplot.plot(x_array, test_voigt)
        pplot.show()

    return








    index_min, index_max = get_min_max_pics(pics)

    print(index_min, index_max)

    x_array = _x_array[index_min:index_max]
    y_array = _y_array[index_min:index_max]

    """pplot.plot(x_array, y_array)"""
    baseline = baseline_(y_array, 10000, 0.0001)

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

        print(pic.x_max)
        print(pic.integral)
        print(pic.fwhm)

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

    fig, (ax1, leg1) = pplot.subplots(ncols=2, gridspec_kw={"width_ratios": [10, 1]})
    fig.suptitle("index min = " + str(index_min) + " index max = " + str(index_max) + " fwhm = " + str(pic.fwhm) + " integral = " + str(pic.integral)
                 + " x_max = " + str(pic.x_max))
    ax1.plot(x_array, y_array)
    ax1.plot(x_array, out.best_fit)
    pplot.show()


class Fitting(QObject):
    finished = pyqtSignal(int)

    def __init__(self, x, y, pics):
        QObject.__init__(self)

        """self.figure = figure
        self.new_figure = None"""

        """ x_datas = []
        y_datas = []
        for i in range(len(self.figure.x_axe.data)):
            x_datas.append(self.figure.x_axe.data[i].data)
            y_datas.append(self.figure.y1_axe.data[i].data)"""

        self.x_datas = x
        self.y_datas = y

        self.pics = []
        self.create_pic(pics)

        self.center = []
        self.area = []
        self.fwhm = []

        index_min, index_max = get_min_max_pics(self.pics)
        self.init_index_min = index_min
        self.init_index_max = index_max

        self.init_center = [pic.center for pic in self.center]

    def create_pic(self, pics):
        for pic in pics:
            n_p = Pic(**pic)
            self.pics.append(n_p)

    def run(self):

        # on fit tous les pics
        for i in range(len(self.x_datas)):
            fit_pics(self.x_datas[i], self.y_datas[i], self.pics, i)

        # self.finished.emit(1)


    """def best_fit(self, pic):
        x_array = pic.slice(self.x_datas[0])
        y_array = pic.slice(self.y_datas[0])

        result_gauss = GaussianModel_fit(x_array, y_array, "cycle0", pic)
        result_voigt = VoigtModel_fit(x_array, y_array, "cycle0", pic)
        result_pseudovoigt = PseudoVoigtModel_fit(x_array, y_array, "cycle0", pic)

        sum_gauss = 0
        sum_voigt = 0
        sum_pseudovoigt = 0
        for param in result_gauss.params:
            try:
                sum_gauss += result_gauss.params[param].stderr / result_gauss.params[param].value
            except TypeError:
                sum_gauss += sys.maxsize

        for param in result_voigt.params:
            if not "_gamma" in param:
                try:
                    sum_voigt += result_voigt.params[param].stderr / result_voigt.params[param].value
                except TypeError:
                    sum_voigt += sys.maxsize

        for param in result_pseudovoigt.params:
            if not "_fraction" in param:
                try:
                    sum_pseudovoigt += result_pseudovoigt.params[param].stderr / result_pseudovoigt.params[param].value
                except TypeError:
                    sum_pseudovoigt += sys.maxsize

        _min = min(sum_gauss, sum_voigt, sum_pseudovoigt)
        if _min == sum_gauss:
            pic.fit = "_GaussianModel"
        elif _min == sum_voigt:
            pic.fit = "_VoigtModel"
        else:
            pic.fit = "_PseudoVoigtModel"""


class Pic:
    def __init__(self, **kwargs):

        self.amplitude = None
        self.center = None
        self.sigma = None
        self.fraction = None
        self.fwhm = None
        self.height = None

        self.left_base = None
        self.right_base = None

        for key, value in kwargs.items():
            self.__setattr__(key, value)

        self.fit = "_PseudoVoigtModel"


    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == "center":
                if self.center * 1.1 < value or self.center / 1.1 > value:
                    print("update discard")
                    return
            elif self.__getattribute__(key) is not None and (self.__getattribute__(key) * 10 < value or
                                                           self.__getattribute__(key) / 10 > value):
                print("update discard")
                return

        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __repr__(self):
        pass


if __name__ == '__main__':
    x_arrays = []
    y_arrays = []

    file = open(r"C:\Users\Maxime\Desktop\export_diffraction.txt", "r")

    data = file.readlines()

    for i in range(len(data)):
        temp = []
        _data_temp = data[i].split("\t")
        for j in range(len(_data_temp)):
            temp.append(float(_data_temp[j]))

        if i % 2 == 0:
            x_arrays.append(temp)
        else:
            y_arrays.append(temp)

    for i in range(len(x_arrays)):
        pplot.plot(x_arrays[i], y_arrays[i])

    pplot.show()

    print(len(x_arrays))

    pplot.plot(x_arrays[0], y_arrays[0])
    pplot.show()

    """def __init__(self, x_max, integral, fwhm, height, sigma, fraction, left_base, right_base):"""
    p1 = {
          'fwhm': 0.040421191883555974,
          'center': 5.15,
          'sigma': 0.08,
          'left_base': 5.1,
          'right_base': 5.225}

    p2 = {'amplitude': 0.00018162457466913028,
          'fwhm': 0.040421191883555974,
          'center': 5.27,
          'sigma': 0.024541345434393236,
          'left_base': 5.2,
          'right_base': 5.3229}

    p3 = {'amplitude': 0.0006180758165759622,
          'fwhm': 0.040421191883555974,
          'center': 5.40,
          'sigma': 0.020210595941777987,
          'left_base': 5.35,
          'right_base': 5.45}

    p4 = {'amplitude': 0.00022113099174519006,
          'fwhm': 0.040421191883555974,
          'center': 5.565635943945343,
          'sigma': 0.024357916389547096,
          'left_base': 5.5,
          'right_base': 5.7}


    pics = [p1, p2, p3, p4]
    fitting = Fitting(x_arrays, y_arrays, pics)
    fitting.run()







