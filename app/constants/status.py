import enum


class STATUS(enum.Enum):
    NEW = 0
    PREPARING = 1
    ON_THE_WAY = 2
    DELIVERED = 3
    RES_CANCELLED = 4
    CUSTOMER_CANCELLED = 5
