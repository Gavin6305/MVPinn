"""
PINN4ME: Physics-Informed Neural Network for Milne-Eddington Inversion

A deep learning approach to solar magnetic field inversion using Physics-Informed Neural Networks.
"""

__version__ = "1.0.0"

from .Training import MEInversionPINN, MEPhysicsLoss, METotalLoss, train_me_pinn
from .DataLoader import prepare_stokes_data, cut_scans
from .Infer import infer_with_pinn, infer_with_pinn_without_fitting
from .process_main import process_ME_inversion_pinn

__all__ = [
    'MEInversionPINN',
    'MEPhysicsLoss',
    'METotalLoss',
    'train_me_pinn',
    'prepare_stokes_data',
    'cut_scans',
    'infer_with_pinn',
    'infer_with_pinn_without_fitting',
    'process_ME_inversion_pinn',
]

