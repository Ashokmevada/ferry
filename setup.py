import setuptools
from typing import List

def get_requirements() -> List[str]:
    """Reads and returns a list of required packages."""
    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            return [
                line.strip() for line in lines
                if line.strip() and line.strip() != "-e ."
            ]
    except FileNotFoundError:
        print("requirements.txt file not found.")
        return []

# Load README for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Metadata
__version__ = "0.1.0"
REPO_NAME = "portfolio-data-pipeline"
AUTHOR_USER_NAME = "Ashokmevada"
SRC_REPO = "ferry_portfolio_pipeline"
AUTHOR_EMAIL = "ashokmevada18@gmail.com"

# Setup
setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="An end-to-end automated portfolio data analysis pipeline using Python, Airflow, SQL, and Power BI.",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=get_requirements()
)
