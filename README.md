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
debug:
```
nuitka --mingw64 --include-package-data=bark --output-dir=dist/ --output-filename=bark --follow-imports src/main.py
```

standalone:
```
nuitka --mingw64 --standalone --include-package-data=bark --disable-console --output-dir=dist/ --output-filename=bark src/main.py
```

onefile:
```
nuitka --mingw64 --onefile --include-package-data=bark --disable-console --output-dir=dist/ --output-filename=bark src/main.py
```

## Virtual Environment
```
python -m venv venv
./venv/Scripts/activate
```
