class BasicUnit:
    def __init__(self, name, fullname=None):
        self.name = name
        if fullname is None:
            fullname = name
        self.fullname = fullname
        self.conversions = dict()






class Data_units:
    def __init__(self, data, unit):
        self.data = data
        self.unit = unit











UNITS = {
    "mode": None,
    "ox/red": None,
    "error": None,
    "control_changes": None,
    "Ns_changes": None,
    "counter_inc.": None,
    "Ns": None,
    "time/s": "secs",
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
    "P/W": None
}

