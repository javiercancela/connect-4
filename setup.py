from setuptools import setup, find_packages

setup(
    name="connect-4",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy==2.2.1",
        "pandas==2.2.3",
        "pyarrow==18.1.0",
        "torch==2.5.1"
    ],
)
