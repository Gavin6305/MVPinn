import torch
import numpy as np
from tqdm import tqdm
from pathlib import Path
from .Training import MEPhysicsLoss
from .DataLoader import prepare_stokes_data
from astropy.io import fits
def infer_with_pinn(model, data_file, output_dir=None, batch_size=64):
    """
    Perform ME inversion using trained PINN model with improved memory management
    
    Parameters: 
        model: Trained ME-PINN model
        data_file (Path): Path to the data file
        output_dir (Path): Directory to save results
        batch_size (int): Batch size for inference
    
    Returns:
        tuple: (parameters_map, stokes_fitted)
    """
    device = next(model.parameters()).device
    
    # Ensure model is in evaluation mode to disable dropout
    model.eval()
    
    # Clear CUDA cache at the beginning
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # Prepare data
    data, wavelengths, hdr = prepare_stokes_data(data_file)
    nx, ny, nw, ns = data.shape
    
    # Create wavelengths tensor
    wavelengths_tensor = torch.tensor(wavelengths, dtype=torch.float32).to(device)
    
    # Initialize output arrays
    parameters_map = np.zeros((nx, ny, 9))
    stokes_fitted = np.zeros((nx, ny, nw, ns))  # Changed shape to match the data
    
    # Physics model for forward prediction
    physics_model = MEPhysicsLoss().to(device)
    
    # Process in batches
    with torch.no_grad():
        for i in tqdm(range(0, nx*ny, batch_size)):
            # Get batch indices
            end_idx = min(i+batch_size, nx*ny)
            batch_size_actual = end_idx - i
            
            # Prepare batch data
            batch_indices = np.unravel_index(np.arange(i, end_idx), (nx, ny))
            batch_data = np.swapaxes(data[batch_indices], 1, 2).reshape(batch_size_actual, -1)
            batch_tensor = torch.tensor(batch_data, dtype=torch.float32).to(device)
            
            # Forward pass
            pred_params = model(batch_tensor)
            
            # Calculate fitted profiles
            stokes_target = torch.tensor(
                np.swapaxes(data[batch_indices], 1, 2), 
                dtype=torch.float32
            ).to(device)
            _, stokes_pred = physics_model(pred_params, wavelengths_tensor, stokes_target)
            
            # Store results
            for j, (x, y) in enumerate(zip(*batch_indices)):
                parameters_map[x, y] = pred_params[j].cpu().numpy()
                # Fix the shape issue - transpose correctly to match expected dimensions
                stokes_fitted[x, y] = np.swapaxes(stokes_pred[j].cpu().numpy(), 0, 1)
            
            # Clear intermediate tensors to free up memory
            del batch_data, batch_tensor, pred_params, stokes_target, stokes_pred
            
            # Optionally clear cache every few batches
            if i % (batch_size * 10) == 0 and torch.cuda.is_available():
                torch.cuda.empty_cache()
    
    # Final cleanup
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        
    # Save results if output_dir is specified
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Save parameters map
        np.savez(
            output_dir / f"me_pinn_params_{Path(data_file).stem}.npz",
            parameters=parameters_map,
            header=dict(hdr)
        )
        
        # Save parameters as FITS
        hdr['COMMENT'] = 'B; theta; chi; eta0; dlambdaD; a; lambda0; B0; B1'
        fits.writeto(
            output_dir / f"me_pinn_params_{Path(data_file).stem}.fits",
            parameters_map,
            header=hdr,
            overwrite=True
        )
        
        # Save fitted profiles
        np.savez(
            output_dir / f"me_pinn_fits_{Path(data_file).stem}.npz",
            stokes_fitted=stokes_fitted,
            wavelengths=wavelengths
        )
    
    return parameters_map, stokes_fitted

def infer_with_pinn_without_fitting(model, data_file, batch_size=64):
    """
    Perform ME inversion using trained PINN model with improved memory management
    
    Parameters: 
        model: Trained ME-PINN model
        data_file (Path): Path to the data file
        batch_size (int): Batch size for inference
    
    Returns:
        parameters_map: Predicted ME parameters
    """
    device = next(model.parameters()).device
    
    # Ensure model is in evaluation mode to disable dropout
    model.eval()
    
    # Clear CUDA cache at the beginning
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # Prepare data
    data, wavelengths, hdr = prepare_stokes_data(data_file)
    nx, ny, nw, ns = data.shape
      
    # Initialize output arrays
    parameters_map = np.zeros((nx, ny, 9))
    
    # Process in batches
    with torch.no_grad():
        for i in tqdm(range(0, nx*ny, batch_size)):
            # Get batch indices
            end_idx = min(i+batch_size, nx*ny)
            batch_size_actual = end_idx - i
            
            # Prepare batch data
            batch_indices = np.unravel_index(np.arange(i, end_idx), (nx, ny))
            batch_data = np.swapaxes(data[batch_indices], 1, 2).reshape(batch_size_actual, -1)
            batch_tensor = torch.tensor(batch_data, dtype=torch.float32).to(device)
            
            # Forward pass
            pred_params = model(batch_tensor)
            
            # Store results
            for j, (x, y) in enumerate(zip(*batch_indices)):
                parameters_map[x, y] = pred_params[j].cpu().numpy()
            
            # Clear intermediate tensors to free up memory
            del batch_data, batch_tensor, pred_params
            
            # Optionally clear cache every few batches
            if i % (batch_size * 10) == 0 and torch.cuda.is_available():
                torch.cuda.empty_cache()
    
    # Final cleanup
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    return parameters_map