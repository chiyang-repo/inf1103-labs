from abc import ABC, abstractmethod 

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be greater than 0 and no more than 100")
        self.__percentage: float = percentage
    
    def apply(self, total: float) -> float:
        return round(total * (1 - self.__percentage / 100), 2)

class StudentDiscount(PercentageDiscount):
    STUDENT_DISCOUNT: float = 5.00
    def __init__(self) -> None:
        super().__init__(self.STUDENT_DISCOUNT)

    def student_discount(self) -> float:
        return self.STUDENT_DISCOUNT

        
class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if threshold <= 0 or amount <= 0:
            raise ValueError("Threshold and amount must be greater than 0")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return round(max(total-self.__amount, 0), 2)
        return total
        

