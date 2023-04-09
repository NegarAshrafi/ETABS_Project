import inspect
import os
import sys
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))
sys.path.append("..")


if __name__ == '__main__':
    
    import Home.Controller as etabs
    drift = etabs.ETABS()
    # Main().run
    # app = QApplication(sys.argv)
    # etabs1 = cntrl
