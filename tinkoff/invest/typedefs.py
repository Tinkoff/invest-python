from typing import Any, NewType, Sequence, Tuple

AccountId = NewType("AccountId", str)
ShareId = NewType("ShareId", str)
ChannelArgumentType = Sequence[Tuple[str, Any]]
