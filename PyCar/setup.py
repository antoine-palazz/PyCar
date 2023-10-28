from setuptools import setup, find_packages

setup(
    name = "PyCar",
    version = "0.0.1",
    author = "Cablant Augustin & Khelifa Naïl & Pogu Thomas",
    author_email = "augustin.cablant@ensae.fr",
    url = "https://github.com/AugustinCablant/PyCar/tree/main/PyCar",
    description = "Package permettant de calculer un itinéraire pour un véhicule électrique en France.",
    packages = find_packages(),
    readme = "READE.md", 
    install_requires = ["numpy == 1.22.4"],  # dans le terminal : pip list | grep numpy
    python_requires = ">= 3.10",
    classifiers = ["Programming Language :: Python :: 3.10" ,
                   "License :: OSI Approved :: MIT License", 
                   "Operating System :: OS Independant"]

)