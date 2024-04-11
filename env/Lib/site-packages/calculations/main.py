import matplotlib.pyplot as plt
import numpy as np
from inspect import getsourcelines


def plotfunc(function, start=0, end=5, points=1000, plot=True, block=True, legend:str=None, title:str=None,
             xlabel:str=None, ylabel:str=None):

    """
    Calculate a function and draw a diagram. Returns function values in y and x.

    :rtype: tuple[np.ndarray, np.ndarray]

    Example:

    plotfunc("x**2", start=0, end=2, points=3)

    -> (array([0., 1., 2.]), array([0., 1., 4.]))
    """
    assert start < end

    x = np.linspace(start, end, points)

    if function.__class__.__name__ == "str":
        y = eval(function)
        label = format(function)

    elif function.__class__.__name__ == "function":
        y = function(x)
        label = getsourcelines(function)

    else:
        raise AttributeError(f"Got {function} but this is not a parameter nor a string")

    if legend is not None:
        label = legend
    if xlabel is None:
        xlabel = "x"
    if ylabel is None:
        ylabel = "y"
    if plot:
        plt.figure(figsize=(10, 5))
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.plot(x, y, 'g', label=label)
        plt.legend()
        plt.grid(True)
        plt.show(block=block)

    return x, y


# plotfunc("x**2", block=False, title="A title")
# plotfunc(lambda x: x ** 2, legend="x^2")
