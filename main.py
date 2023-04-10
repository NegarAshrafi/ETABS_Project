import inspect
import os
import sys
from pathlib import Path

''' TODO: If you need to do these actions, better to put it in a different
module and import it here
'''
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))
sys.path.append("..")


if __name__ == '__main__':

    '''TODO: Create an Application'''

    '''TODO: Move import to top of module'''
    import Home.Controller as etabs

    '''TODO: choose better name for your parameters, maybe better to use Home
    for first window.'''
    drift = etabs.ETABS()
    # Main().run
    # app = QApplication(sys.argv)
    # etabs1 = cntrl
