# Quick Start Guide

This guide will help you get started with PINN4ME quickly.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd PINN4ME

# Create conda environment
conda create -n PINN-torch python=3.8
conda activate PINN-torch

# Install dependencies
pip install -r requirements.txt

# Install package in development mode (RECOMMENDED)
# This allows you to import 'src' from anywhere
pip install -e .
```

**Note**: If you don't install the package, you'll need to run the setup cell in the example notebook first, or manually add the repository root to your Python path.

## Basic Usage

### 1. Training a Model

```python
from src import train_me_pinn

# Train a new model
model = train_me_pinn(
    data_file='path/to/your/stokes_data.fts',
    n_epochs=100,
    batch_size=32,
    learning_rate=1e-3,
    optimizer_type='adam'
)
```

### 2. Loading a Pre-trained Model

```python
import torch
from src import MEInversionPINN

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MEInversionPINN(n_wavelengths=50).to(device)
model.load_state_dict(torch.load('path/to/model.pt'))
model.eval()
```

### 3. Running Inference

```python
from src import infer_with_pinn

# Perform inference
parameters_map, stokes_fitted = infer_with_pinn(
    model,
    'path/to/your/stokes_data.fts',
    output_dir='results/'
)

# Extract magnetic field components
B = parameters_map[..., 0]  # Field strength
theta = parameters_map[..., 1]  # Inclination
chi = parameters_map[..., 2]  # Azimuth

# Calculate Bx, By, Bz
import numpy as np
Bx = B * np.cos(chi) * np.sin(theta)
By = B * np.sin(chi) * np.sin(theta)
Bz = B * np.cos(theta)
```

### 4. Complete Workflow

See `examples/example.ipynb` for a complete example that includes:
- Data loading
- Model training
- Inference
- Visualization

## Data Requirements

Your FITS file should contain:
- 4D array: `[nx, ny, nwavelengths, 4]`
- Last dimension: Stokes I, Q, U, V profiles
- Header keywords: `STARTWV`, `ENDWV`, `CDELT1`, `CDELT2`

## Troubleshooting

### CUDA Out of Memory
- Reduce `batch_size` in training or inference
- Use `infer_with_pinn_without_fitting()` for faster inference

### Import Errors
- Make sure you're in the correct conda environment
- Install package: `pip install -e .`
- Or add the src directory to your Python path

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [examples/example.ipynb](examples/example.ipynb) for complete workflows
- See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute

