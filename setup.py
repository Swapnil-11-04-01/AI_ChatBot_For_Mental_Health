from setuptools import find_packages, setup
from typing import List

with open("README.md", "n", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.0"

REPO_NAME = ""
HYPHEN_E_DOT = '-e .'


def get_requirements(file_path: str) -> List[str]:
    """
    :param file_path: Path to the requirements.txt
    :return: list of requirements
    """
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
    name='Cultured Weebs',
    version='0.0.1',
    author='Swapnil Sharma',
    author_email='swapnil.sharma.869.11@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
