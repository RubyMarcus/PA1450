import matplotlib as plt
from data import data
import matplotlib.pyplot as plt


class Generate:
    def __init__(self):
        self.weather_data = data(65090)

    def generate_chart(self, period, condition):
        data = self.weather_data.get_data(condition, period)

        data.plot(x='date', kind='bar')
        plt.show()

    def generate_graph(self, period, condition):
        data = self.weather_data.get_data(condition, period)

        data.plot(x='date')
        plt.show()

    def generate_report(self, period, condition):
        code, title = condition[0]
        data = self.weather_data.get_data(condition, period)
        print(period, title, "are", " approximately ", data[title].mean())
