# Troubleshooting

## ModuleNotFoundError: No module named 'src'

If you encounter this error when running the example notebook, try one of these solutions:

### Solution 1: Run the Setup Cell (Easiest)

The example notebook includes a setup cell at the beginning (Cell 2). **Make sure to run this cell first** before importing from `src`. This cell automatically adds the repository root to your Python path.

### Solution 2: Install the Package (Recommended for Development)

From the repository root directory:

```bash
cd /path/to/PINN4ME
pip install -e .
```

This installs the package in "editable" mode, allowing you to import `src` from anywhere.

### Solution 3: Manual Path Setup

If the above don't work, add this at the beginning of your notebook or script:

```python
import sys
from pathlib import Path

# Add repository root to Python path
repo_root = Path(__file__).parent.parent if '__file__' in globals() else Path('..').resolve()
sys.path.insert(0, str(repo_root))
```

### Solution 4: Change Working Directory

If running from Jupyter, make sure your working directory is the repository root:

```python
import os
os.chdir('/path/to/PINN4ME')
```

## Other Common Issues

### CUDA Out of Memory

- Reduce `batch_size` in training or inference
- Use `infer_with_pinn_without_fitting()` for faster inference
- Process data in smaller chunks

### Import Errors After Installation

- Make sure you're in the correct conda environment: `conda activate PINN-torch`
- Reinstall: `pip install -e . --force-reinstall`
- Check Python version: `python --version` (should be 3.8+)

### Data File Not Found

- Check that your FITS file path is correct
- Verify the file has the correct format (4D array: [nx, ny, nw, 4])
- Check FITS header contains required keywords: `STARTWV`, `ENDWV`, `CDELT1`, `CDELT2`

## Getting Help

If you continue to experience issues:
1. Check the [QUICKSTART.md](QUICKSTART.md) guide
2. Review the [examples/README.md](examples/README.md)
3. Open an issue on GitHub with:
   - Error message
   - Python version
   - Operating system
   - Steps to reproduce

