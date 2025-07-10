from setuptools import setup, find_packages

setup(
    name='mlsecure',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mlsecure = mlsecure.cli:main',
        ],
    },
)
