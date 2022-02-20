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
    "dq/mA.h": None,
    "(Q-Qo)/mA.h": None,
    "control/V/mA": None,
    "Ecell/V": "volt",
    "I_Range": None,
    "<I>/mA": "milliampere",
    "x": None,
    "Q_discharge/mA.h": None,
    "Q_charge/mA.h": None,
    "Capacity/mA.h": None,
    "Efficiency/%": None,
    "control/V": "volt",
    "control/mA": "milliampere",
    "cycle_number": None,
    "P/W": None,


    # nom complet de toutes les unitées
    "centimeters": "cm",
    "inches": "inch",
    "radians": "radians",
    "degrees": "deg",
    "Hertz": "hertz",
    "seconds": "secs",
    "minutes": "minutes",
    "hours": "hours",
    "volt": "volt",
    "millivolt": "millivolt",
    "ampere": "ampere",
    "milliampere": "milliampere",
    
    
    # nom court des unitée
    "cm": "cm",
    "inch": "inch",
    "hertz": "hertz",

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

    def convert_value_to(self, value, unit):
        conversion_fn = self.conversions[unit]
        ret = conversion_fn(value)
        return ret

    def get_unit(self):
        return self

    def get_units_available(self):
        return [key for key in self.conversions.keys()]


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

    def create_units(self):

        cm = BasicUnit('cm', 'centimeters')
        inch = BasicUnit('inch', 'inches')

        inch.add_conversion_factor(cm, 2.54)
        cm.add_conversion_factor(inch, 1 / 2.54)

        """--------------------------------------------------"""

        radians = BasicUnit('rad', 'radians')
        degrees = BasicUnit('deg', 'degrees')

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
            func = self.unit.conversions[unit]
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
        return str(self.data) + " in " + self._unit.name

    def append(self, obj):
        if not isinstance(obj, float) and not isinstance(obj, int):
            raise ValueError
        else:
            self.data.append(obj)

    def set_units(self):
        if isinstance(self.unit, str):
            u = Units()
            self.unit = u[self.unit]

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
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    units = Units()

    data_test = Data_unit(data, units["cm"])
    data_test2 = Data_unit(data, units["cm"])

    print(data_test2.unit.name)

    data_test.extend(data_test2)

    print(data_test)

    if 1.2 in data_test:
        print("ok")

    del data_test[2]

    data_test.convert_to(units["inch"])

    for value in data_test:
        print(value)

    print(UNITS["time/h"])
    print(UNITS["cycle_number"])
