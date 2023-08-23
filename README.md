## Running the project locally
### Install Torch and CUDA
Go to [https://pytorch.org/get-started/locally/](), choose the appropriate options, and run the command that is generated.

Note: can also be run without CUDA, but it will be much slower to generate speech.

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
I've been building with MSVC, which can be installed through Visual Studio Installer. The --msvc switch can be removed if you want Nuitka to figure out which compiler to use.

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
