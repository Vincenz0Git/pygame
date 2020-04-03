### DOS game in Python (WIP) ###

Description of the game here: https://www.mattelgames.com/en/cards/dos

Trying to figure out how to implement it using pygame, more to come


### On OSX ###

Pygame did not work for me with the brew version of Python3:

```console
Poured from bottle on 2020-03-20 at 10:03:14
From: https://github.com/Homebrew/homebrew-core/blob/master/Formula/python.rb
==> Dependencies
Build: pkg-config ✔
Required: gdbm ✔, openssl@1.1 ✔, readline ✔, sqlite ✔, xz ✔
==> Options
--HEAD
	Install HEAD version
```

It worked with the miniconda version, installed with the bash script found in:

```html
https://docs.conda.io/en/latest/miniconda.html
```

dependencies:

- pygame

### Demo ###

Game in console with local input/output

```console
python demo/demogame.py
```

### Without GUI ###

From the pygame folder:

Launch the server:

```console
python GameServer.py
```

Launch the clients

```console
python GameClient.py
```

From the clients: /help to have the info
