from setuptools import setup, find_packages

version = "0.0.7"

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = [x.strip() for x in f if x.strip()]

# with open("test_requirements.txt", "r", encoding="utf-8") as f:
#     test_requires = [x.strip() for x in f if x.strip() and not x.startswith("-r")]

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
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="aws, crawler",
    package_dir={"": "cloud_products"},
    packages=find_packages(where="cloud_products"),  # Required
    python_requires=">=3.5, <4",
    install_requires=install_requires,
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={"dev": ["check-manifest"], "test": ["coverage"],},
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],  # Optional
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={"console_scripts": ["sample=sample:main",],},  # Optional
)
