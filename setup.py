from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name         = 'todoster',
    version      = '1.0.0',
    author       = 'Sophie Au',
    author_email = 'some.person@web.de',
    license      = 'MIT',
    description  = 'A simple command line todo list.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords     = ['command-line-tool', 'productivity', 'todo', 'task-manager'],
    url          = 'https://github.com/sophieau/todoster',

    packages     = ['todoster'],
    zip_safe     = False,
    entry_points = {
        'console_scripts': ['todoster=todoster.__main__:main'],
    },
    python_requires  = '>=3.6',
    install_requires = [
        'isoweek >= 1.3.3',
    ]
)
