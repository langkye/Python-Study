# Author:  Langkye
# Data:    2019/9/30

import os, sys
DIR = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(DIR)))

from ATM.core import main

if __name__ == '__main__':
    main.run()