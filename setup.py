import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('requirements-dev.txt') as f:
    tests_requirements = [line for line in f.read().splitlines() if '-r ' not in line]

setuptools.setup(
    name="postcodes",
    version="0.1.0",
    author="Samuel Sampaio",
    author_email="samukasmk@gmail.com",
    license="Apache 2.0",
    description="Library to parse postal code format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samukasmk/postcodes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=["scripts/postcodes"],
    install_requires=install_requires,
    setup_requires='pytest-runner',
    tests_require=tests_requirements,
    test_suite='setup.test_suite',
)
