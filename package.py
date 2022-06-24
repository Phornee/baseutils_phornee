name = "baseutils_phornee"

version = "3.0.0"

authors = ["Ismael Raya"]

requires = [
    "python-3.8+"
]

build_command = "python {root}/install.py" # Run this command on `rez build`

def commands():
    env.PYTHONPATH.append("{root}/baseutils_phornee")
    