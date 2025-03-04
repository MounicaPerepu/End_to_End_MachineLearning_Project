from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    """
    This function reads the requirements.txt file and returns the list of requirements
    """
    requirements=[]
    with open(file_path) as f:
        requirements=f.readlines()
        requirements=[req.replace('\n','') for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements  

setup(
    name='End_to_End_MachineLearning_Project',
    version='0.0.1',
    author='Mounica Perepu',
    author_email='mounica.perepu@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)