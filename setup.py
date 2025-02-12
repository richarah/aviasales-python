from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='aviasales-python',
    version='1.0.0',
    packages=find_packages(),
    install_requires=required,
    author="Richard Alexander Haydon",
    author_email="richarah@stud.ntnu.no",
    description="Python wrapper for Aviasales API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/richarah/aviasales-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)