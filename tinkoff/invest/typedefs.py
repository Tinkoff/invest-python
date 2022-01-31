from typing import Any, NewType, Sequence, Tuple

AccountId = NewType("AccountId", str)
ChannelArgumentType = Sequence[Tuple[str, Any]]
