from setuptools import setup

setup(
    version='0.0.2',
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'tychos-cli=tychos.cli:main',
        ],
    },
)