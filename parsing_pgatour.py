    """
    This file is intended to be used for parsing out all of the stats on pgatour.com/stats and adding them to pandas dataframes

    """

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame