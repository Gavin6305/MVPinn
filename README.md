# PINN4ME: Physics-Informed Neural Network for Milne-Eddington Inversion

A deep learning approach to solar magnetic field inversion using Physics-Informed Neural Networks (PINNs) for Milne-Eddington (ME) inversion of Stokes profiles.

## Overview

This project implements a Physics-Informed Neural Network (PINN) for performing Milne-Eddington inversion of solar Stokes profiles. The neural network learns to predict ME parameters (magnetic field strength, inclination, azimuth, etc.) from observed Stokes I, Q, U, V profiles, while being constrained by the physics of the ME forward model.

## Key Features

- **Physics-Informed Architecture**: The ME forward model is integrated into the neural network, allowing end-to-end training with physics constraints
- **Efficient Training**: Uses PyTorch for GPU-accelerated training
- **Batch Processing**: Supports batch inference for large datasets
- **Flexible Input**: Works with FITS files containing Stokes profiles

## Architecture

The model consists of:
- **Neural Network Encoder**: Fully connected network that maps flattened Stokes profiles to ME parameters
- **ME Physics Model**: Differentiable implementation of the Milne-Eddington forward model using PyTorch
- **Physics-Informed Loss**: Combined loss function that enforces both data fidelity and physics constraints

### Model Details

- **Input**: Flattened Stokes profiles `[batch_size, 4*n_wavelengths]`
- **Output**: 9 ME parameters per pixel:
  - B: Magnetic field strength [0, 4500] G
  - θ: Inclination [0, π]
  - χ: Azimuth [0, π]
  - η₀: Line-to-continuum opacity ratio [0.5, 20]
  - ΔλD: Doppler width [0.12, 0.25] Å
  - a: Damping parameter [0, 10]
  - λ₀: Line center shift [-0.25, 0.25] Å
  - B₀, B₁: Source function parameters

## Installation

### Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended)
- Conda (for environment management)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd PINN4ME
```

2. Create and activate the conda environment:
```bash
conda create -n PINN-torch python=3.8
conda activate PINN-torch
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Training

```python
from src import train_me_pinn
from pathlib import Path

# Train a new model
model = train_me_pinn(
    data_file='path/to/stokes_data.fts',
    n_epochs=100,
    batch_size=32,
    learning_rate=1e-3,
    optimizer_type='adam'
)
```

### Inference

```python
from src import MEInversionPINN, infer_with_pinn
import torch

# Load trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MEInversionPINN(n_wavelengths=50).to(device)
model.load_state_dict(torch.load('path/to/model.pt'))
model.eval()

# Perform inference
parameters_map, stokes_fitted = infer_with_pinn(
    model, 
    'path/to/stokes_data.fts',
    output_dir='results/'
)
```

### Complete Workflow

See `examples/example.ipynb` for a complete example of training and inference.

## Project Structure

```
PINN4ME/
├── src/                    # Source code
│   ├── Training.py        # Model definition and training
│   ├── DataLoader.py      # Data loading and preprocessing
│   ├── Infer.py           # Inference functions
│   ├── process_main.py    # Main processing pipeline
│   ├── ME_utils.py        # ME model utilities
│   └── visualization.py   # Visualization utilities
├── examples/              # Example notebooks
│   └── example.ipynb      # Main example
├── docs/                  # Documentation
├── tests/                 # Unit tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Data Format

The code expects FITS files with the following structure:
- 4D array: `[nx, ny, nwavelengths, 4]` where the last dimension contains Stokes I, Q, U, V
- FITS header should contain:
  - `STARTWV`: Starting wavelength
  - `ENDWV`: Ending wavelength
  - `CDELT1`, `CDELT2`: Pixel scales

## Citation

If you use this code in your research, please cite:

```bibtex
@software{pinn4me,
  title={PINN4ME: Physics-Informed Neural Network for Milne-Eddington Inversion},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/PINN4ME}
}
```

## License

[Specify your license here]

## Acknowledgments

- BBSO/NIRIS for observational data
- PyTorch team for the deep learning framework

## Contact

For questions or issues, please open an issue on GitHub or contact [your email].

# MVPinn
