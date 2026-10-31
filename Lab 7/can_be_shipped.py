from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self): # Any class that can be shipped must provide a way to calculate its shipping cost
        pass