class MovingAverageStrategyState:
    def __init__(self):
        self._long_open: bool = False
        self._short_open: bool = False
        self._position: int = 0

    @property
    def long_open(self) -> bool:
        return self._long_open

    @property
    def short_open(self) -> bool:
        return self._short_open

    @property
    def position(self) -> int:
        return self._position
