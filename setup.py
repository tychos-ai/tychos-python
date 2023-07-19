from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    version='0.1.0',
    description='Python client library for the Tychos API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
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