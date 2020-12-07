import setuptools

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testtp", 
    version="0.0.1",
    author="Be5yond",
    author_email="beyond147896@126.com",
    description="Http client for testers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Be5yond/testtp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "pytest", "schema", "loguru"],
    python_requires='>=3.6'
)
