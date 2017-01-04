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

    def summary(self):
        """
        Summary
        Print out the statistical summary after all data are backtested.
        """
        pass


