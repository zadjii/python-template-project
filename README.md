# Python Project Template

This repo serves as a blank template for a python project in the way I usually
write python projects.
* It is set up to use the `Instance` object to manage the SqlAlchemy database
  and load application config.
* There are two placeholder models in the `models/` directory, as an example of
  how DB models should be authored.
* It also includes all the migration (update the database version) and
  reset/repopulate scripts
* It has some helpers that I really like in `common/`, especially
  `ResultAndData` for returning bot a suceeded/failed boolean and some sort of
  return value.
* It's also got a sample in `argparse-main.py` for setting up a `main` that uses
  subcommands to run the program, so you can quickly build a git-like
  commandline experience.


## Contributing

After cloning the repo, run `pip install -r requirements.txt`

### Code formatting

This project uses [`black`](https://github.com/psf/black) for code formatting.
To format the code, run `black .`. You might need to add your python scripts
directory to your path. For me, this was done with:

```
set PATH=%PATH%;%localappdata%\Packages\PythonSoftwareFoundation.Python.3.7_qbz5n2kfra8p0\LocalCache\local-packages\Python37\Scripts
```
