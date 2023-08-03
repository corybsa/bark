import torch

print(f'PyTorch version: {torch.version}')

if torch.cuda.is_available():
	print(f'CUDA is available，version is:{torch.version.cuda}')
	if torch.backends.cudnn.is_available():
		print(f'cuDNN is available，version is:{torch.backends.cudnn.version()}')
	else:
		print('cuDNN Not Available')
else:
	print('CUDA Not Available')

if torch.cuda.is_available():
	a = torch.tensor(1, device='cuda')
	b = torch.tensor(2, device='cuda')
	print(a + b)
else:
	a = torch.tensor(1)
	b = torch.tensor(2)
	print(a + b)
