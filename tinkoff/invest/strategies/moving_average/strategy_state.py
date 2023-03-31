class MovingAverageStrategyState:
    def __init__(self) -> None:
        self._long_open: bool = False
        self._short_open: bool = False
        self._position: int = 0

    @property
    def long_open(self) -> bool:
        return self._long_open

    @long_open.setter
    def long_open(self, value: bool) -> None:
        self._long_open = value

    @property
    def short_open(self) -> bool:
        return self._short_open

    @short_open.setter
    def short_open(self, value: bool) -> None:
        self._short_open = value

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        self._position = value
