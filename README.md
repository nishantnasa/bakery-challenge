# Bakery Challenge

## Installation / Environment setup
### pyenv

Install pyenv unless you already have it installed.

```
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

### python

Install python unless you already have it installed.

```
pyenv install 2.7.6
pyenv rehash
pyenv versions
```

### pyenv virtualenv

Install pyenv-virtualenv unless you already have it installed.

```
git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
echo 'export VIRTUAL_ENV_DISABLE_PROMPT=1' >> ~/.zshrc
source ~/.zshrc
```

### Project setup - local
#### Cloning git repo

```
git clone https://github.com/nishantnasa/bakery-challenge.git
```

#### Create virtualenv

Move to the root directory of project `bakery-challenge`, if not already there. Create virtual environment for the project. 

```
cd bakery-challenge
pyenv virtualenv 2.7.6 bakery-challenge-2.7.6
pyenv local bakery-challenge-2.7.6
pyenv versions
```

#### install requirements / modules

Install python modules.

```
pip install -r requirements.txt
```

## Run / Test
### Run

Run the app from root directory `bakery-challenge`. 

```
python main.py
```

### Test
#### DocTest

```
python -m doctest -v main.py
```