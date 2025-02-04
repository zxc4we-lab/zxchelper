from setuptools import setup, find_packages

setup(
    name="zxchelper",  # Replace with your package name
    version="0.1.0",    # Version number
    author="zxc4we",
    author_email="zxc4we028@gmail.com",
    description="Helpul package to requests and selenium with undetected",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zxc4we-lab/zxchelper",  # Link to your repo
    packages=find_packages(),  # Automatically find packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify Python version requirements
    install_requires=["selenium_driverless","requests"],      # List dependencies here
)