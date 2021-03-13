from os.path import join
import setuptools

__version__ = ''
exec(open(join('edfpy', 'version.py')).read())
requirements = open('requirements.txt').read().split('\n')

setuptools.setup(
    name='edfpy',
    version=__version__,
    packages=setuptools.find_packages(),
    author='Justus Schwabedal, John Snyder',
    maintainer='Justus Schwabedal',
    maintainer_email='jschwabedal@gmail.com',
    description="Lean EDF Reader",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
