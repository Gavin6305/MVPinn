# Contributing to PINN4ME

Thank you for your interest in contributing to PINN4ME! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/PINN4ME.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

1. Create a conda environment:
```bash
conda create -n PINN-torch python=3.8
conda activate PINN-torch
```

2. Install the package in development mode:
```bash
pip install -e .
```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

## Testing

Before submitting a pull request, please ensure:
- All existing tests pass
- New tests are added for new functionality
- Code is properly documented

## Pull Request Process

1. Update the README.md if needed
2. Update CHANGELOG.md with your changes
3. Ensure all tests pass
4. Request review from maintainers

## Questions?

Feel free to open an issue for any questions or concerns.

