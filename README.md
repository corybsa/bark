## Installation
### Torch and CUDA
Go to [https://pytorch.org/get-started/locally/]() and run the command that is generated.

For Windows it would be:
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

### Bark
> pip install git+https://github.com/suno-ai/bark.git

## Build
To build the exe, run `python -m PyInstaller --onefile ./main.py`

## Virtual Environment
python -m venv venv
./venv/Scripts/activate
