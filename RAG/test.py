import torch

# 检查 CUDA 是否可用
cuda_available = torch.cuda.is_available()

if cuda_available:
    print(f"CUDA is available. GPU: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available.")
