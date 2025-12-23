import torch
import numpy as np
from pathlib import Path
import glob
import os
from .DataLoader import prepare_stokes_data
from .Training import MEInversionPINN, train_me_pinn
from .Infer import infer_with_pinn

# -----------------------------Main Function--------------------------------
def process_ME_inversion_pinn(data_folder, model_path=None, output_dir=None, 
                             n_epochs=100, batch_size=32, validation_split=0.1,
                             inference_batch_size=64,
                             activation='tanh', optimizer_type='adam', sample_index=0,
                             dropout_rate=0.2, weight_decay=1e-5):
    """
    Process ME inversion using PINN with a single data file
    
    Parameters:
        data_folder (str): Path to the input data folder
        model_path (str): Path to trained model (if None, train new model)
        output_dir (Path): Directory to save results
        n_epochs (int): Number of training epochs
        batch_size (int): Batch size for training
        validation_split (float): Fraction of data to use for validation
        inference_batch_size (int): Batch size for inference
        activation (str): Activation function to use
        optimizer_type (str): Optimizer to use ('adam' or 'lbfgs')
        sample_index (int): Index of the sample to use for training and inference
        dropout_rate (float): Dropout rate for regularization (0.0 to disable)
        weight_decay (float): L2 regularization factor (0.0 to disable)
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Get data files and select the one to be used
    data_files = glob.glob(os.path.join(data_folder, '*.fts'))
    data_files.sort()
    
    if not data_files:
        raise ValueError(f"No data files found in {data_folder}")
    
    sample_index = min(sample_index, len(data_files) - 1)
    training_file = data_files[sample_index]
    print(f"Selected file for training: {training_file}")
    
    # Get wavelength information from the file
    data, wavelengths, _ = prepare_stokes_data(training_file)
    _, _, nw, _ = data.shape
    
    # Load or train model
    if model_path and Path(model_path).exists():
        print(f"Loading model from {model_path}")
        model = MEInversionPINN(nw, activation=activation, dropout_rate=dropout_rate).to(device)
        model.load_state_dict(torch.load(model_path, map_location=device))
    else:
        print(f"Training new model with {activation} activation using {optimizer_type} optimizer")
        model = train_me_pinn(
            training_file, 
            n_epochs=n_epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            activation=activation,
            optimizer_type=optimizer_type,
            dropout_rate=dropout_rate,
            weight_decay=weight_decay
        )
    
    # Important: Set model to eval mode for inference to disable dropout
    model.eval()
    
    # Perform inference on the same file
    print(f"Performing inference on {training_file}")
    parameters_map, stokes_fitted = infer_with_pinn(model, training_file, output_dir, batch_size=inference_batch_size)
        
    # Extract magnetic field components
    B = parameters_map[..., 0]
    theta = parameters_map[..., 1]
    chi = parameters_map[..., 2]
    
    Bx = B * np.cos(chi) * np.sin(theta)
    By = B * np.sin(chi) * np.sin(theta)
    Bz = B * np.cos(theta)
    
    print(f"ME-PINN inversion complete for file: {training_file}")
    return parameters_map, stokes_fitted

# Example usage with a single file
if __name__ == "__main__":
    from pathlib import Path
    import glob

    # Set file paths
    # data_folder = Path('/research/bs644/ql47/NIRIS/20240725_cals_recalibrated')
    data_folder = Path('/research/bs644/ql47/NIRIS/20180729_cal')
    # output_dir = Path('/project/bs644/ql47/ME/Example/pinn_results_recalibrated')
    output_dir = Path('/project/bs644/ql47/ME/Example/pinn_results_20180729_cal')
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Process the file with simplified model
    results = process_ME_inversion_pinn(
        data_folder, 
        output_dir=output_dir,
        n_epochs=60,                # More epochs may be needed for the simplified model
        batch_size=256,              # Smaller batch size for better generalization
        inference_batch_size=256,
        validation_split=0.2,
        activation='tanh',
        optimizer_type='adam',
        sample_index=1,              # Use the first file
        dropout_rate=0,            # Add regularization with dropout
        weight_decay=1e-5            # Add L2 regularization
    )

