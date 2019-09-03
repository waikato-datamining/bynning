from typing import TypeVar, Hashable

# The type of the items in the bins. Must be binnable
ItemType = TypeVar("ItemType", bound="Binnable[KeyType]")

# The type of the data used to determine the bin an object
# goes into
KeyType = TypeVar("KeyType")

# The type of the bin labels (must be hashable as
# is used to store bins in a map)
LabelType = TypeVar("LabelType", bound=Hashable)
