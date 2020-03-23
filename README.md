# bynning
Python library for sorting arbitrary data into bins.

## Core Classes/Concepts

This section provides an explanation of the core classes and concepts that underpin the bynning model.

### Binnable

```python
from wai.bynning import Binnable
```

An object is **Binnable** if it conforms to the `wai.bynning.Binnable` interface. The interface provides a `bin_key`
property, which can be of any type, and represents the data used to decide which bin the object belongs in.

### BinItem

```python
from wai.bynning import BinItem
```

A **BinItem** is a wrapper for objects that aren't inherently binnable. This allows arbitrary objects to be sorted
using the **bynning** system. A **BinItem** is initialised with a payload object (the object being binned) and a
provided **bin-key** object. Static methods are provided for bulk wrapping/unwrapping of objects with **BinItem**
wrappers.

### Bin

```python
from wai.bynning import Bin
```

A **Bin** represents a collection of objects that have been sorted into a group based on their **bin-key**. Each bin
has a **Label**, which is the 'name' of the **Bin**. **Bins** can be iterated through, and retain the order in which
they were filled.

### Binning

```python
from wai.bynning import Binning
```

A **Binning** is the result of sorting a collection of items into a number of **Bins**. A **Binning** can be iterated
over the **Bins** it contains, or over the items in those **Bins**.

### Binner

```python
from wai.bynning.binners import Binner
```

A **Binner** is an algorithm for determining which **Bin** an object should go into based on its **bin-key**. The
`wai.bynning.binners` package provides many implementations of common binning algorithms. **Binners** support one
public method, `bin`, which takes an iterable of **Binnable** objects to bin and returns the resulting **Binning**.

### Extractor

```python
from wai.bynning.extraction import Extractor
```

**Extractors** are used in a few places to determine which information is relevant to a given operation. For example,
determining the **bin-key** of a non-**Binnable** object when wrapping it in a **BinItem**.

## Examples

### Grouping Containers by Size 

```python
from typing import Sized, Iterable, Dict, List

# The containers we want to group
containers: Iterable[Sized] = ...

# Wrap the containers in BinItems, keyed by their size
from wai.bynning import BinItem
from wai.bynning.extraction import SizeExtractor
binnable_containers: Iterable[BinItem] = BinItem.extract_from(SizeExtractor(), containers)

# As the bin-key is the containers size, just need to bin by bin-key
from wai.bynning import Binning
from wai.bynning.binners import KeyBinner
container_binning: Binning = KeyBinner().bin(binnable_containers)

# Create a dictionary from container-size to containers
containers_by_size: Dict[int, List[Sized]] = {
    bin.label: list(BinItem.unwrapping_iterator(bin))
    for bin in container_binning
}
```