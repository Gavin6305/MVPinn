"""
Basic import tests to verify package structure
"""

def test_import_main_modules():
    """Test that main modules can be imported"""
    from src import (
        MEInversionPINN,
        MEPhysicsLoss,
        METotalLoss,
        train_me_pinn,
        prepare_stokes_data,
        infer_with_pinn,
        process_ME_inversion_pinn
    )
    assert MEInversionPINN is not None
    assert MEPhysicsLoss is not None
    assert METotalLoss is not None
    assert train_me_pinn is not None
    assert prepare_stokes_data is not None
    assert infer_with_pinn is not None
    assert process_ME_inversion_pinn is not None

def test_model_initialization():
    """Test that model can be initialized"""
    from src import MEInversionPINN
    import torch
    
    n_wavelengths = 50
    model = MEInversionPINN(n_wavelengths=n_wavelengths)
    
    assert model is not None
    # Test forward pass with dummy data
    dummy_input = torch.randn(1, n_wavelengths * 4)
    output = model(dummy_input)
    assert output.shape == (1, 9)  # 9 ME parameters

if __name__ == "__main__":
    test_import_main_modules()
    test_model_initialization()
    print("All tests passed!")

