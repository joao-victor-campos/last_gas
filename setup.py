from setuptools import setup, find_packages

__version__ = "0.2.0"

with open("README.md") as description_file:
    readme = description_file.read()

with open("requirements.txt") as requirements_file:
    requirements = [line for line in requirements_file]

setup(
    name="last_gas",
    version=__version__,
    author="Menzolas",
    python_requires=">=3.8.5",
    description="Last Gas Discord Bot",
    long_description=readme,
    install_requires=requirements,
    packages=find_packages(),
)
