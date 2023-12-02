# Vollgas Config

Config tool provides basic configuration file locating, loading and validation.

## Usage

```
from vollgas_config.config import Config
config = Config("app.yaml", (".", f'{os.path.expanduser("~")}/.app', "/etc", "/usr/local/etc"))
```

## Install from Git

pip install git+https://chriskauffman@bitbucket.org/chriskauffman/vollgas-config.git@v2.0.0
pip install git+https://chriskauffman@bitbucket.org/chriskauffman/vollgas-config.git@v0.1.1


## Poetry Ubuntu Linux Install

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
