import matplotlib.pyplot as plt
import numpy as np
import datetime
from decimal import Decimal


class Strategy:
    """
    Strategy
    """
    def __init__(self, logger):
        """
        Constructor
        :param logger: Logger
        """
        self.logger = logger
        self.graph = None

    def open_order(self, **kwargs):
        """
        Open order
        :param kwargs: Named arguments
        :return: None if no order is opened; Otherwise an order object is returned.
        """
        return None

    def close_order(self, order, **kwargs):
        """
        Close order
        :param order: The opened order
        :param kwargs: Named arguments
        :return: None if the order is not settled; Otherwise a settled order object is returned
        """
        return None

    def summary(self, **kwargs):
        """
        Summary
        Print out the statistical summary after all data are backtested.
        """
        pass

    @classmethod
    def plot_graph(cls, date_time, price, graph=None):
        """
        Plot the graph
        :param graph: MatPlotLibGraph
        :param date_time: Date time
        :param price: Price
        """
        date_time = (date_time - datetime.datetime(1970, 1, 1)).total_seconds()
        if graph is None:
            graph = plt.scatter([date_time], [price])
            plt.xlim([date_time, date_time + 60 * 60 * 24])
            # plt.ylim([float(price) * 0.95, float(price) * 1.05])
            plt.draw()
            plt.pause(0.1)
        else:
            array = graph.get_offsets()
            array = np.append(array, [date_time, price])
            graph.set_offsets(array)
            # plt.xlim([array[::2].min() - 0.5, array[::2].max() + 0.5])
            plt.ylim([float(array[1::2].min()) - 0.5, float(array[1::2].max()) + 0.5])
            plt.draw()
            plt.pause(0.1)

        return graph

    @classmethod
    def plot_show(cls, block=True):
        plt.show(block=block)


