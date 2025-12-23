# Repository Structure

```
PINN4ME/
├── .github/
│   └── workflows/
│       └── python-package.yml    # GitHub Actions CI
├── docs/                          # Documentation (to be added)
├── examples/
│   └── example.ipynb              # Example usage notebook
├── src/                           # Source code
│   ├── __init__.py               # Package initialization
│   ├── Training.py                # Model definition and training
│   ├── DataLoader.py             # Data loading utilities
│   ├── Infer.py                   # Inference functions
│   ├── process_main.py           # Main processing pipeline
│   ├── ME_utils.py               # ME model utilities
│   └── visualization.py          # Visualization utilities
├── tests/
│   └── test_imports.py           # Basic import tests
├── .gitignore                     # Git ignore rules
├── CHANGELOG.md                   # Version history
├── CONTRIBUTING.md                # Contribution guidelines
├── LICENSE                        # MIT License
├── QUICKSTART.md                  # Quick start guide
├── README.md                      # Main documentation
├── requirements.txt               # Python dependencies
└── setup.py                      # Package setup
```

## Key Files

- **src/Training.py**: Core neural network model and training functions
- **src/DataLoader.py**: FITS file loading and preprocessing
- **src/Infer.py**: Inference and prediction functions
- **src/process_main.py**: High-level processing pipeline
- **examples/example.ipynb**: Complete usage example

## Installation

```bash
pip install -r requirements.txt
# or
pip install -e .
```

## Usage

```python
from src import train_me_pinn, infer_with_pinn

# Train
model = train_me_pinn('data.fts', n_epochs=100)

# Infer
params, stokes = infer_with_pinn(model, 'data.fts')
```
