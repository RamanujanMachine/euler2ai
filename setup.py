from setuptools import find_packages, setup


setup(
    name="unifier",
    version="0.0.1",
    description="Library for unifying formulas",
    package_dir={"": "unifier"},
    packages=find_packages(where="unifier"),
    install_requires=[
        "gmpy2>=2.2.1",
        "matplotlib>=3.10.1",
        "mpmath>=1.3.0",
        "networkx>=3.4.2",
        "numpy>=2.2.4",
        "sympy>=1.13.3"
        ],
    python_requires=">=3.10",
)
