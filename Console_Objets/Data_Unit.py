import copy
import math

UNITS = {
    # nom des données du fichier txt
    "mode": None,
    "ox/red": None,
    "error": None,
    "control_changes": None,
    "Ns_changes": None,
    "counter_inc.": None,
    "Ns": None,
    "time/h": "hours",
    "dq/mA.h": "milliampere_heure",
    "(Q-Qo)/mA.h": "milliampere_heure",
    "Q_charge/discharge/mA.h": "milliampere_heure",
    "dQ/C": "coulomb",
    "(Q-Qo)/C": "coulomb",
    "half_cycle": None,
    "control/V/mA": "volt_par_milliampere",
    "Ecell/V": "volt",
    "I_Range": None,
    "<I>/mA": "milliampere",
    "I/mA": "milliampere",
    "x": None,
    "Q_discharge/mA.h": "milliampere_heure",
    "Q_charge/mA.h": "milliampere_heure",
    "Capacity/mA.h": "milliampere_heure",
    "Efficiency/%": "pourcentage",
    "control/V": "volt",
    "control/mA": "milliampere",
    "cycle_number": None,
    "P/W": None,

    # nom complet de toutes les unitées
    "centimeters": "cm",
    "inches": "inch",
    "radians": "radians",
    "degrees": "degrees",
    "Hertz": "hertz",
    "seconds": "secs",
    "minutes": "minutes",
    "hours": "hours",
    "volt": "volt",
    "millivolt": "millivolt",
    "ampere": "ampere",
    "milliampere": "milliampere",
    "pourcentage": "pourcentage",
    "milliampere_heure": "milliampere_heure",
    "volt_par_milliampere": "volt_par_milliampere",
    "milliampere_heure_par_gramme": "milliampere_heure_par_gramme",
    "coulomb_par_gramme": "coulomb_par_gramme",
    "coulomb": "coulomb",
    "degree_c": "degree_c",
    "kelvin": "kelvin",

    # nom court des unitée
    "cm": "cm",
    "inch": "inch",
    "hertz": "hertz",
    "mA": "milliampere",
    "A": "ampere",
    "V": "volt",
    "mV": "millivolt",
    "s": "secs",
    "min": "minutes",
    "h": "hours",
    "g": "gramme",
    "kg": "killogramme",
    "mA.h/g": "milliampere_heure_par_gramme",
    "mAh/g": "milliampere_heure_par_gramme",
    "C": "coulomb",
    "C/g": "coulomb_par_gramme",
    "mA.h": "milliampere_heure",
    "°": "degrees",
    "°C": "degree_c",
    "K": "kelvin",
    "rad": "radians",
    # nom des unitées sans conversion

    "%": "pourcentage",
    "ua": "ua",

    "Energy_charge/W.h": None,
    "Energy_discharge/W.h": None,
    "Capacitance_charge/µF": None,
    "Capacitance_discharge/µF": None,


}


class BasicUnit:
    def __init__(self, name, fullname=None):
        self.name = name
        if fullname is None:
            fullname = name
        self.fullname = fullname
        self.conversions = dict()

    def add_conversion_factor(self, unit, factor):
        def convert(x):
            return x * factor

        self.conversions[unit] = convert

    def add_conversion_fn(self, unit, fn):
        self.conversions[unit] = fn

    def get_conversion_fn(self, unit):
        return self.conversions[unit]

    def get_conversion(self, unit):
        return self.conversions[unit]

    def get_unit(self):
        return self

    def get_units_available(self):
        return [key for key in self.conversions.keys()]


class CompositeUnit:
    def __init__(self, unit1, facteur, unit2, name, fullname=None):
        self.name = name
        if fullname is None:
            fullname = name
        self.fullname = fullname

        self.unit1 = unit1
        self.unit2 = unit2

        self.facteur = facteur

        self.conversions_unit1 = dict()
        self.conversions_unit2 = dict()

        for key, func in unit1.conversions.items():
            self.conversions_unit1[key] = func

        for key, func in unit2.conversions.items():
            self.conversions_unit2[key] = func

    def get_conversion(self, unit):
        try:
            conversion_fn = self.conversions_unit1[unit]
        except KeyError:
            conversion_fn2 = self.conversions_unit2[unit]

            conversion_fn = lambda x: conversion_fn2(x)

        return conversion_fn


class Units:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls.units = {}
            cls.create_units(cls)

        return cls._instance

    def __getitem__(self, item):
        if item is None:
            return None
        elif isinstance(item, str):
            name = UNITS[item]
            return self.units[name]
        else:
            raise TypeError('Invalid argument type: {}'.format(type(item)))

    def get_unit(self, name):
        name = UNITS[name]
        if name is None:
            return None
        else:
            return self.units[name]

    def create_units(self):

        cm = BasicUnit('cm', 'centimeters')
        inch = BasicUnit('inch', 'inches')

        inch.add_conversion_factor(cm, 2.54)
        cm.add_conversion_factor(inch, 1 / 2.54)

        """--------------------------------------------------"""

        radians = BasicUnit('rad', 'radians')
        degrees = BasicUnit('°', 'degrees')

        radians.add_conversion_factor(degrees, 180.0 / math.pi)
        degrees.add_conversion_factor(radians, math.pi / 180.0)

        """--------------------------------------------------"""

        hertz = BasicUnit('Hz', 'Hertz')
        secs = BasicUnit('s', 'seconds')
        minutes = BasicUnit('min', 'minutes')
        hours = BasicUnit('h', 'hours')

        hertz.add_conversion_fn(secs, lambda x: 1. * x)
        hertz.add_conversion_factor(minutes, lambda x: x * 60.0)
        hertz.add_conversion_factor(hours, lambda x: x * 3600.0)

        secs.add_conversion_fn(hertz, lambda x: 1. / x)
        secs.add_conversion_factor(minutes, 1 / 60.0)
        secs.add_conversion_factor(hours, 1 / 3600.0)

        minutes.add_conversion_fn(hertz, lambda x: 1. / x / 60)
        minutes.add_conversion_factor(secs, 60.0)
        minutes.add_conversion_factor(hours, 1 / 60.0)

        hours.add_conversion_fn(hertz, lambda x: 1. / x / 3600)
        hours.add_conversion_factor(secs, 3600.0)
        hours.add_conversion_factor(minutes, 60.0)

        """--------------------------------------------------"""

        volt = BasicUnit('V', 'volt')
        millivolt = BasicUnit('mV', 'millivolt')

        millivolt.add_conversion_factor(volt, 1 / 1000.0)
        volt.add_conversion_factor(millivolt, 1000.0)

        """--------------------------------------------------"""

        ampere = BasicUnit('A', 'ampere')
        milliampere = BasicUnit('mA', 'milliampere')

        milliampere.add_conversion_factor(ampere, 1 / 1000.0)
        ampere.add_conversion_factor(milliampere, 1000.0)

        """--------------------------------------------------"""

        gramme = BasicUnit('g', 'gramme')
        killogramme = BasicUnit('kg', 'killogramme')

        gramme.add_conversion_factor(killogramme, 1 / 1000.0)
        killogramme.add_conversion_factor(gramme, 1000.0)

        """--------------------------------------------------"""

        milliampere_heure = BasicUnit('mA.h', 'mA.h')
        coulomb = BasicUnit('C', 'coulomb')

        milliampere_heure.add_conversion_factor(coulomb, 1 / 3.6)
        coulomb.add_conversion_factor(milliampere_heure, 3.6)

        """--------------------------------------------------"""

        milliampere_heure_par_gramme = BasicUnit('mAh/g', 'mAh/g')
        coulomb_par_gramme = BasicUnit('C/g', 'C/g')

        milliampere_heure_par_gramme.add_conversion_factor(coulomb_par_gramme, 1 / 3.6)
        coulomb_par_gramme.add_conversion_factor(milliampere_heure_par_gramme, 3.6)

        """--------------------------------------------------"""

        degree_c = BasicUnit('°C', '°C')
        kelvin = BasicUnit('K', 'kelvin')

        degree_c.add_conversion_fn(kelvin, lambda x: x - 273.15)
        kelvin.add_conversion_fn(degree_c, lambda x: x + 273.15)

        """--------------------------------------------------"""

        # déclaration des unitées non convertibles
        pourcentage = BasicUnit('%', 'pourcentage')
        volt_par_milliampere = BasicUnit('V/mA', 'V/mA')
        ua = BasicUnit("ua", "Arbitrary Unit")


        # définition des unités
        self.units["cm"] = cm
        self.units["inch"] = inch

        self.units["hertz"] = hertz
        self.units["secs"] = secs
        self.units["minutes"] = minutes
        self.units["hours"] = hours

        self.units["volt"] = volt
        self.units["millivolt"] = millivolt

        self.units["ampere"] = ampere
        self.units["milliampere"] = milliampere

        self.units["gramme"] = gramme
        self.units["killogramme"] = killogramme

        self.units["degrees"] = degrees
        self.units["radians"] = radians

        self.units["milliampere_heure"] = milliampere_heure
        self.units["coulomb"] = coulomb

        self.units["milliampere_heure_par_gramme"] = milliampere_heure_par_gramme
        self.units["coulomb_par_gramme"] = coulomb_par_gramme

        self.units["degree_c"] = degree_c
        self.units["kelvin"] = kelvin

        self.units["pourcentage"] = pourcentage

        self.units["volt_par_milliampere"] = volt_par_milliampere
        self.units["ua"] = ua


    def add_unit(self, name):
        """
        On ajoute une unité à self.units
        Utilise pour la no'malisation, l'unité aura un nom mais aucune conversion ne sera
        disponible

        :param name: nom de la nouvelle unité
        :return: None
        """
        if name in self.units:
            return

        UNITS[name] = name
        unit = BasicUnit(name)
        self.units[name] = unit


class Data_unit(list):
    def __init__(self, array=None, unit=None):
        super().__init__()
        self.ptr = 0

        if array is None:
            self._data = []
        else:
            self._data = array

        self._unit = unit

    def convert_to(self, unit):
        if unit == self.unit or self.unit is None:
            return
        try:
            func = self.unit.get_conversion(unit)
            self.data = [func(value) for value in self.data]
            self._unit = unit
        except KeyError:
            raise ValueError('cannot convert ' + self.unit.name + ' in ' + unit.name)



    def __getitem__(self, item):
        if isinstance(item, slice):
            start, stop, step = item.indices(len(self))
            if stop >= len(self.data):
                raise IndexError
            return self.data[start:stop]
        elif isinstance(item, int):
            return self.data[item]
        elif isinstance(item, tuple):
            raise NotImplementedError('Tuple as index')
        else:
            raise TypeError('Invalid argument type: {}'.format(type(item)))

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        self.ptr = 0
        return self

    def __next__(self):
        if self.ptr == len(self.data):
            raise StopIteration
        s = self.data[self.ptr]
        self.ptr += 1
        return s

    def __contains__(self, obj):
        if not isinstance(obj, float) and not isinstance(obj, int):
            raise ValueError
        else:
            for value in self.data:
                if value == obj:
                    return True
            return False

    def __delitem__(self, index):
        if not isinstance(index, int):
            raise ValueError
        else:
            del self.data[index]

    def __repr__(self):
        if self._unit is None:
            return str(self.data) + " in None"
        else:
            return str(self.data) + " in " + self._unit.name

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def append(self, obj):
        if not isinstance(obj, float) and not isinstance(obj, int):
            raise ValueError
        else:
            self.data.append(obj)

    def set_units(self):
        if isinstance(self.unit, str):
            u = Units()
            self.unit = u.get_unit(self.unit)

    def copy(self):
        new_data_unit = Data_unit()

        new_data_unit.data = [value for value in self.data]

        units = Units()
        new_data_unit.unit = units.get_unit(self.unit.name)

        return new_data_unit

    @property
    def unit(self):
        return self._unit

    @property
    def data(self):
        return self._data

    @unit.setter
    def unit(self, _unit):
        self._unit = _unit

    @data.setter
    def data(self, _data):
        self._data = _data


if __name__ == '__main__':
    from Console_Objets.Figure import Figure
    f1 = Figure("f1")


    data = [1, 2, 3, 4, 5]
    f1.add_data_x(data, None, None, None)


    print(f1.__dict__)

