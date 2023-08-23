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

### Nuitka
standalone:
```
nuitka --msvc="14.3" --lto=no --standalone --include-package-data=bark --noinclude-data-files="torch/include" --noinclude-data-files="torch/lib" --output-dir=dist/ --output-filename=bark src/main.py
```

onefile:
```
tbd
```

## Virtual Environment
```
python -m venv venv
./venv/Scripts/activate
```
