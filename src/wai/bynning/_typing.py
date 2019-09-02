from typing import TypeVar, Hashable

# The type of the bin-key. The bin-key is the data that is used
# to determine which bin a binnable object will go into
KeyType = TypeVar("KeyType")

# The type of the binned item
ItemType = TypeVar("ItemType")

# The type of the bin labels (must be hashable as
# is used to store bins in a map)
LabelType = TypeVar("LabelType", bound=Hashable)
