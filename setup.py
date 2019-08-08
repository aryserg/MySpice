 
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MySpice",
    version="0.0.2",
    author="Mikhail Lukyanov",
    author_email="free4telecom@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LukyanovM/MySpice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    install_requires=[
    'PySpice',
    'numpy',
    'dataclasses',
    ],
)
