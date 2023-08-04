## Installation
### Torch and CUDA
Go to [https://pytorch.org/get-started/locally/]() and run the command that is generated.

For Windows it would be:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

then run installing from requirements.txt:
```
pip install -r requirements.txt
```

## Build
To build the exe, run 
```
pyinstaller --onefile --name wgbark --paths venv/Lib/site-packages --hidden-import=pytorch --collect-data torch --copy-metadata torch --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata numpy --copy-metadata tokenizers --copy-metadata filelock --copy-metadata huggingface-hub --copy-metadata safetensors cli.py
```

## Virtual Environment
```
python -m venv venv
./venv/Scripts/activate
```

## Nuitka
debug:
```
nuitka --standalone --output-dir=dist/nuitka/ --output-filename=wgbark cli.py
```

prod:
```
nuitka --standalone --onefile --output-dir=dist/nuitka/ --output-filename=wgbark cli.py
```
