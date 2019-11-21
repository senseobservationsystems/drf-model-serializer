import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drf-model-serializer",
    version="0.0.1",
    author="Panji Y. Wiwaha",
    author_email="panjiyudasetya@gmail.com",
    description="A simple library that enhance 'ModelSerializer' class so that it performs object-level validation for free.",
    keywords=['django', 'drf', 'serializer'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/senseobservationsystems/drf-model-serializer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'django',
        'djangorestframework'
    ]
)
