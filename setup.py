import setuptools

BASE_REQUIREMENTS = ["SQLAlchemy==2.0.21", "pydantic==2.4.2"]

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="sqlorm",
    version="NEXT_VERSION",
    packages=setuptools.find_packages(include=["pydbantic"], exclude=["build"]),
    author="Joshua Jamison",
    author_email="joshjamison1@gmail.com",
    description="'db' within pydantic - A single model for shaping, creating, accessing, storing data within a Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codemation/pydbantic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Pydantic",
        "Framework :: FastAPI",
        "Topic :: Database",
    ],
    python_requires=">=3.7, <4",
    install_requires=BASE_REQUIREMENTS,
    extras_require={
        "all": BASE_REQUIREMENTS
        + POSTGRES_REQUIREMENTS
        + MYSQL_REQUIREMENTS
        + LITE_REQUIREMENTS,
        "postgres": POSTGRES_REQUIREMENTS,
        "mysql": MYSQL_REQUIREMENTS,
        "sqlite": LITE_REQUIREMENTS,
    },
)
