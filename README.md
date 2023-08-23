## Running the project locally
### Create and activate virtual environment
```
python -m venv venv
./venv/Scripts/activate
```

### Install Torch and CUDA
!!! This needs to be done before installing pip requirements, because pip will think that torch is already installed and not install the correct version. !!!

Go to [https://pytorch.org/get-started/locally/](), choose the appropriate options, and run the command that is generated.

Note: can also be run without CUDA, but it will be much slower to generate speech.

For Windows it would be:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Install pip requirements
Then install packages from requirements.txt:
```
pip install -r requirements.txt
```

### Run the project
```
python src/main.py
```

## Building From Source
### Nuitka
I've been building with MSVC, which can be installed through Visual Studio Installer. The --msvc switch can be removed if you want Nuitka to figure out which compiler to use.

standalone:
```
nuitka --msvc="14.3" --lto=no --standalone --include-package-data=bark --noinclude-data-files="torch/include" --noinclude-dlls="torch/*" --output-dir=dist/ --output-filename=bark src/main.py
```

onefile:
```
nuitka --msvc="14.3" --lto=no --onefile --disable-console --include-package-data=bark --noinclude-data-files="torch/include" --noinclude-dlls="torch/*" --output-dir=dist/ --output-filename=bark src/main.py
```

## Installing a fresh venv
```
deactivate
rm -r venv
python -m venv venv
./venv/Scripts/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```
