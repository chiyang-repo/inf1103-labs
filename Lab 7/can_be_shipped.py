from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self): # calculate shipping cost based on weight and shipping rates
        pass