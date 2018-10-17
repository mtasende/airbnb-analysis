import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def prop_vs_mean(x, y):
    """
    Proportional dependency vs "taking the mean" comparison.
    It is used to decide the method to imput missing data.
    """
    data = pd.concat([x, y], axis=1).dropna(how='any')
    x = data[x.name]
    y = data[y.name]

    a = (y.values / x.values).mean()
    plt.scatter(x, y, label='Data')
    plt.hlines(y.mean(), x.min(), x.max(), colors='r', label='Mean')
    x_t = np.linspace(x.min(), x.max(), 1000)
    plt.plot(x_t, a * x_t, 'g', label='Proportional')
    plt.legend()


def show_data(data):
    """ Shows shape, missing data, and head of a pandas DataFrame. """
    print('The data has shape: {}\n'.format(data.shape))
    print('There is {} missing data!\n'.format(data.isnull().sum().sum()))
    print(data.head())


