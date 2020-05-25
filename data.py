import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# karlskrona station id 65090

"""
Parmeter which key to use (int):

1. Lufttemperatur = 1
2. Daggpunktstemperatur = 39
3. Nederbördsmängd = 7
4. Relativ luftfuktighet = 6
5. Vindhastighet = 4
6. Vindriktning = 3
7. Max av medel vindhastighet = 25 // maybe not this one (problem parsing with json)
8. Byvind = 21
9. Total molnmängd = 16
10. Signifikanta moln = ? // didnt find this one
11. Lägsta molnbas = 36
12. Lägsta molnbas, min(15 min) = 37 # (problem parsing with json)
13. Solskenstid = 10 # (problem parsing with json)
14. Globalstrålning = ? / didnt find this one
15. Långvägsstrålning = 24 / maybe not this one (problem parsing with json) 
16. Lufttryck reducerat havsytans nivå = 9
17. Sikt = 12
18. Rådande väder = 13

" Current working list"
1. Lufttemperatur = 1 (celsius)
2. Daggpunktstemperatur = 39 (celsius)
3. Nederbördsmängd = 7 (mm)
4. Relativ luftfuktighet = 6 (procent)
5. Vindhastighet = 4 (m/s)
6. Vindriktning = 3 (grader)
    0 till 360 grader (När vindhastigheten är 0 m/s sätts vindriktningen till 0 grader. 360 grader representerar norr, 90 grader öster osv.
7. Byvind = 21 (m/s)
8. Total molnmängd = 16 (procent)
9. Lägsta molnbas = 36 (m)
10. Lufttryck reducerat havsytans nivå = 9 (pascal)
11. Sikt = 12 (m)
12. Rådande väder = 13 (kodvärden)

Periods:
1. latest-hour
2. latest-day
3. latest-months
"""


class data:

    def __init__(self, station):
        self.station = station
        self.data_frames = []
        self.parameter_names = []

    def get_data(self, parameters, period):
        """
        This function will retrieve data from smhi api. Since they only allow specific periods such as 'latest-hour,
        latest-day, latest-month' its kinda limited. You can only download one parameter at time as well that is why we
        are using a for loop to download multiple parameters.

        :param parameters:
        :param period:
        :return:
        """

        self.parameter_names.clear()
        self.data_frames.clear()

        for parameter in parameters:
            parameter_code, parameter_name = parameter

            self.parameter_names.append(parameter_name)

            url = "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/" \
                  "{parameter}/station/65090/period/{period}/data.json".format(parameter=parameter_code, period=period)

            try:
                response = requests.get(url, timeout=2)

                self.prepare_data(response, parameter_name)
            except requests.exceptions.RequestException:
                raise Exception('Connection failed.') from None

        if len(parameters) == 2:
            return self.merge_data()
        return self.data_frames[0]

    def prepare_data(self, response, parameter_name):
        """
        Convert response to data frame.

        :param response:
        :param parameter_name:
        :return:
        """

        data_ = response.json()['value']

        df = pd.DataFrame.from_dict(data_)

        df['date'] = pd.to_datetime(df['date'], unit='ms')

        df['value'] = df['value'].astype(float)

        renamed_df = df.rename(columns={'value': parameter_name})

        self.data_frames.append(renamed_df)

    def merge_data(self):
        """
        Merge two parameters of separate data frames to one.

        :return:
        """

        df_one = self.data_frames[0]
        df_two = self.data_frames[1]

        df_one[self.parameter_names[1]] = df_two[self.parameter_names[1]]

        print(df_one)

        return df_one
