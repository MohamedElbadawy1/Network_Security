from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    """
    this function will return list of requirements

    """
    requirements: List[str] = []
    try:
        with open('requirements.txt','r') as f:
            #read line from file
            lines = f.readlines()
            
            for line in lines:
                #strip the line and add to requirements list
                if line != '-e .'and line != '\n':
                    requirements.append(line.strip())
            

    except FileNotFoundError:
        print("requirements.txt file not found")    

    return requirements

setup(
    name="Network_Security",
    version="0.0.1",
    author="Mohamed Elbadawy",
    author_email="mohamed.asaad.elbadawy@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)


