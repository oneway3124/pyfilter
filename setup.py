from setuptools import setup


setup(
    name='pyfilter',
    version='0.0.1',
    author='Victor Tingström',
    author_email='victor.tingstrom@gmail.com',
    description='Package for performing online Bayesian inference in state space models',
    packages=['datamodels'],
    install_requires=[
        'numpy>=1.11.3',
        'matplotlib>=2.0.0',
        'pandas>=0.19.2',
        'scipy>=0.18.1'
    ]
)