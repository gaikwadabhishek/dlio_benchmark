#!/bin/bash
# Minimal DLIO install for client nodes (Python 3.8 compatible)
# Skips pydftracer, tensorflow, nvidia-dali which require Python 3.9+
#
# Usage: ./install_client.sh

set -e

echo "Installing DLIO benchmark (minimal, client-node mode)..."

# Install DLIO without pulling in dependencies
pip install --no-deps .

# Install core deps that work on Python 3.8
pip install \
  aistore \
  mpi4py \
  numpy \
  h5py \
  "hydra-core>=1.3.2" \
  omegaconf \
  pandas \
  psutil \
  "Pillow>=9.3.0" \
  PyYAML \
  torch \
  torchvision \
  torchaudio

echo ""
echo "Verifying installation..."
python3 -c "from aistore.sdk import Client; print('  aistore SDK: OK')"
python3 -c "import torch; print('  PyTorch: OK')"
python3 -c "from dlio_benchmark.storage.aistore_storage import AIStoreStorage; print('  AIStore storage: OK')"
which dlio_benchmark > /dev/null && echo "  dlio_benchmark CLI: OK"

echo ""
echo "Installation complete!"
