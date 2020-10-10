from setuptools import setup, find_packages

version = "1.1.1"

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = [x.strip() for x in f if x.strip()]

setup(
    name="cloud-products",
    version=version,
    description="A package for getting cloud product descriptions from the provider website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dylanhogg/cloud-products",
    author="Dylan Hogg",
    author_email="dylanhogg@gmail.com",
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable ",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="aws, crawler",
    package_dir={"": "cloud_products"},
    packages=find_packages(where="cloud_products"),
    python_requires=">=3.6, <4",
    install_requires=install_requires,
)
