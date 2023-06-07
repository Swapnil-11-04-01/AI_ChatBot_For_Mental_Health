from setuptools import find_packages, setup
from typing import List

with open("README.md", "n", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.0"

REPO_NAME = "AI_ChatBot_For_Mental_Health"
AUTHOR_USER_NAME = 'Swapnil-11-04-01'
SRC_REPO = ''
AUTHOR_EMAIL = "swapnil.sharma.869.11@gmail.com"

setup(
    name=REPO_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="AI Chatbot, named EVE AI, for thebetterment of the mental health.",
    long_description=long_description,
    long_descrption_content="text/markdown",
    url=(f'https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}'),
    project_url={"Bug Tracker": f'https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues'},
    package_dir={"": "src"},
    packages=find_packages(where="src")
)
