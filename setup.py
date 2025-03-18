from setuptools import find_packages, setup


setup(
    name="unifier",
    version="0.0.1",
    description="Library for unifying formulas",
    packages=['unifier', 'unifier.utils', 'unifier.utils.LIReC_utils'],
    install_requires=[
        'gmpy2==2.2.1',
        'ipython==9.0.2',
        'matplotlib==3.10.1',
        'mpmath==1.3.0',
        'networkx==3.4.2',
        'numpy==2.2.4',
        'openai==1.66.3',
        'pydantic==2.10.6',
        'sympy==1.13.3',
        'tiktoken==0.9.0',
        ],
    python_requires=">=3.10",
)
