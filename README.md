## Running the project locally
### Install Torch and CUDA
Go to [https://pytorch.org/get-started/locally/]() and run the command that is generated.

For Windows it would be:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Install requirements
Then install packages from requirements.txt:
```
pip install -r requirements.txt
```

## Building From Source

### PyInstaller
To build the exe, run 
```
pyinstaller --onefile --name bark --paths venv/Lib/site-packages --hidden-import=pytorch --collect-data torch --copy-metadata torch --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata numpy --copy-metadata tokenizers --copy-metadata filelock --copy-metadata huggingface-hub --copy-metadata safetensors main.py
```
### Nuitka
debug:
```
nuitka --lto=no --mingw64 --standalone --output-dir=dist/ --output-filename=bark --include-package-data=bark --noinclude-pytest-mode=nofollow --noinclude-setuptools-mode=nofollow main.py
```

prod:
```
nuitka --lto=no --mingw64 --onefile --output-dir=dist/ --output-filename=main --include-package-data=bark --noinclude-pytest-mode=nofollow --noinclude-setuptools-mode=nofollow main.py
```

## Virtual Environment
```
python -m venv venv
./venv/Scripts/activate
```
