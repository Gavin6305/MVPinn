import numpy as np
import astropy.io.fits as fits
import torch

def polyfit_torch(x, y, degree):
    """
    Polynomial fitting using PyTorch's linear algebra operations
    """
    # Create Vandermonde matrix
    vander = torch.stack([x**i for i in range(degree, -1, -1)], dim=1)
    
    # Solve the least squares problem
    coeffs = torch.linalg.lstsq(vander, y).solution
    
    return coeffs

def polyval_torch(coeffs, x):
    """
    Evaluate polynomial using PyTorch operations
    """
    result = torch.zeros_like(x)
    for i, coeff in enumerate(coeffs):
        result += coeff * x**(len(coeffs) - 1 - i)
    return result

def prepare_stokes_data(data_file):
    """
    Prepare Stokes profiles data from FITS file
    
    Parameters:
        data_file (Path): Path to the input data file
    
    Returns:
        tuple: (data, wavelengths, header)
    """
        
    with fits.open(data_file) as hdul:
        b = hdul[0].data
        hdr = hdul[0].header

    # Ensure native byte order before converting to torch tensor
    b = np.ascontiguousarray(b, dtype=b.dtype.newbyteorder('='))
    
    # Convert to torch tensor and move to GPU if available
    b = torch.from_numpy(b).float()  # Convert to float type
    if torch.cuda.is_available():
        b = b.cuda()
    
    b = b.permute(3, 2, 1, 0)  # Equivalent to np.swapaxes

    nx, ny, nw = b.shape[0:3]
    l_step = (hdr['ENDWV'] - hdr['STARTWV']) / (nw - 1)
    dlambda = torch.arange(nw, device=b.device, dtype=torch.float32) * l_step + hdr['STARTWV']
    # Find line center position
    aver_prof0 = torch.mean(b[..., 0].reshape(-1, nw), dim=0)
    
    x = torch.arange(nw, device=b.device, dtype=torch.float32)
    coeffs = polyfit_torch(x, aver_prof0, 2)
    yfit = polyval_torch(coeffs, x)
    aver_prof = aver_prof0 - yfit + torch.mean(yfit)
    ind = torch.argmin(aver_prof)
    
    lambda_shift = dlambda[ind] if abs(dlambda[ind]) > l_step else 0
    if abs(lambda_shift) > 1.:
        raise ValueError('Lambda Shift is too large')
    
    dlambda = dlambda - lambda_shift
    # Select wavelength range
    s = torch.where(abs(dlambda) <= 2.0)[0]
    c = torch.where((abs(dlambda) >= 1.5) & (abs(dlambda) <= 2.0))[0]

    # get the residual of the continuum for profile Q and U only*********
    continuum_mean_Q = torch.mean(b[..., c, 1], dim=2, keepdim=True)  # Keep dim=2 to get (nx, ny, 1)
    continuum_mean_U = torch.mean(b[..., c, 2], dim=2, keepdim=True)  # Keep dim=2 to get (nx, ny, 1)

    b[..., :, 1] = b[..., :, 1] - continuum_mean_Q  # Now both have shape (nx, ny, nw)
    b[..., :, 2] = b[..., :, 2] - continuum_mean_U  # Now both have shape (nx, ny, nw)
    # Get normalization factor
    factor = torch.median(b[..., 40 if 40 < nw else nw-1, 0])
    
    b = b[:, :, s, :] / factor
    
    # Move wavelengths to CPU before returning
    dlambda = dlambda[s].cpu()
    
    return b, dlambda, hdr

def cut_scans(data, hdr, cut_off=33):
    """
    Cut scans if the ENDWV is greater than 6.0 Angstroms
    Equivalent to the IDL function CUT_SCANS
    
    Parameters:
        data: Input data array
        hdr: FITS header
        cut_off: Index to cut at (default: 33)
        
    Returns:
        tuple: (trimmed_data, updated_header)
    """
    # Calculate wavelength array
    l_step = (hdr['ENDWV'] - hdr['STARTWV']) / (hdr['NAXIS3'] - 1)
    dlambda = np.arange(hdr['NAXIS3']) * l_step + hdr['STARTWV']
    
    # Cut the data
    trimmed_data = data[..., :cut_off+1, :]
    
    # Update header
    hdr_copy = hdr.copy()
    hdr_copy['NAXIS3'] = cut_off + 1
    hdr_copy['ENDWV'] = dlambda[cut_off]
    
    return trimmed_data, hdr_copy