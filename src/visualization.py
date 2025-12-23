import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
def visualize_Bx_By_Bz(results, output_dir):
    # Print keys of results
    print(results.keys())

    parameters_map = results['parameters']
    stokes_fitted = results['stokes_fitted']
    PINN_wavelengths = results['wavelengths']

    Bfield = parameters_map[:, :, 0]
    theta = parameters_map[:, :, 1]
    chi = parameters_map[:, :, 2]
    eta0 = parameters_map[:, :, 3]
    dlambdaD = parameters_map[:, :, 4]
    a = parameters_map[:, :, 5]
    lambda0 = parameters_map[:, :, 6]
    Bx = Bfield * np.cos(chi) * np.sin(theta)
    By = Bfield * np.sin(chi) * np.sin(theta)
    Bz = Bfield * np.cos(theta)
    # plot Bx By Bz
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    axs[0].imshow(Bx, cmap='gray',vmin=-1500,vmax=1500,origin='lower')
    axs[0].set_title('Bx')
    axs[1].imshow(By, cmap='gray',vmin=-1500,vmax=1500,origin='lower')
    axs[1].set_title('By')
    axs[2].imshow(Bz, cmap='gray',vmin=-1500,vmax=1500,origin='lower')
    axs[2].set_title('Bz')
    plt.tight_layout()
    plt.savefig(output_dir / 'Bfield.png',dpi=300)
    plt.show()
    return Bx, By, Bz