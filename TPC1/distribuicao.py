import matplotlib.pyplot as plt
import numpy as np

class Distribuicao:
    def __init__(self, pontos = {}, title="", x_axis = "", y_axis = ""):
        self.pontos = pontos
        self.traducoes = {}
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.title = title

    def add_ponto(self, ponto, traducao = None):
        if ponto[0] in self.pontos:
            raise ValueError("Value already exists in distribuition")

        self.pontos[ponto[0]] = ponto[1]
        self.traducoes[ponto[0]] = traducao if traducao else ponto[0]


    def __normalize_length__(self, s, n):
        m = len(s)
        for i in range(0, n-m):
            s = s + " "

        return s

    def to_table(self):
        x_lengths = [len(self.x_axis)] + [len(str(self.traducoes[k])) for k in self.pontos]
        y_lengths = [len(self.y_axis)] + [len(str(self.pontos[k])) for k in self.pontos]
        first_col_length = max(x_lengths) + 1 #+1 for padding
        second_col_length = max(y_lengths) + 1 #+1 for padding
        total_length = first_col_length + second_col_length + 3
        splitter = "+" + "-" * (total_length - 2) + "+"
        x = [self.__normalize_length__(str(self.traducoes[k]), first_col_length)
             for k in self.pontos]
        y = [self.__normalize_length__(str(self.pontos[k]), second_col_length)
             for k in self.pontos]
        x_header = self.__normalize_length__(self.x_axis, first_col_length)
        y_header = self.__normalize_length__(self.y_axis, second_col_length)
        data = list(map(lambda a: f"|{a[0]}|{a[1]}|", zip(x,y)))
        lines = [self.title] + [splitter] + [f"|{x_header}|{y_header}|"] + [splitter] + \
            data + [splitter]

        ans = ""
        for line in lines:
            ans += line + "\n"

        return ans[:-1] #Remove the last "\n" from the string

    def to_bar_chart(self):
        distribution = np.array([self.pontos[k] for k in self.pontos])
        labels = [self.traducoes[k] for k in self.pontos]
        plt.bar(labels, distribution)
        plt.legend(title=self.title)
        plt.show()

    def to_pie_chart(self):
        distribution = np.array([self.pontos[k] for k in self.pontos])
        labels = [self.traducoes[k] for k in self.pontos]
        plt.pie(distribution, labels = labels)
        plt.legend(title=self.title)
        plt.show()