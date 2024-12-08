import torch

print("CUDA Available:", torch.cuda.is_available())
print("CUDA Device Count:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("CUDA Device Name:", torch.cuda.get_device_name(0))
    print("CUDA Version:", torch.version.cuda)
    print("PyTorch CUDA Version:", torch.version.__version__)
else:
    print("No CUDA-compatible GPU detected.")