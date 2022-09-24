from setuptools import setup

setup (
    name="wsh-modules",
    version = "0.1",
    author="NickRodriguez",
    author_email="nick@dashanddata.com",
    description = "weather app models, sqlalchemy, and config objects",
    packages=['wsh_config','wsh_models'],
    python_requires=">=3.6",
    )