# Examples

This directory contains example notebooks demonstrating how to use PINN4ME.

## Running the Examples

### Option 1: Install the package (Recommended)

From the repository root:

```bash
cd /path/to/PINN4ME
pip install -e .
```

Then you can import directly:
```python
from src import MEInversionPINN, train_me_pinn
```

### Option 2: Use the setup cell

The example notebook includes a setup cell at the beginning that automatically adds the repository root to the Python path. Just run the first cell before importing.

### Option 3: Manual path setup

If the above don't work, you can manually add the path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('..').resolve()))  # Go up one level from examples/
```

## Notebooks

- `example.ipynb` - Complete example showing training and inference workflow

