# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cgitb
from UI_interface import Main_windows_UI


if __name__ == '__main__':
    cgitb.enable(format='text')
    main = Main_windows_UI.Main_interface()

