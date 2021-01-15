import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()


setup(
    name='interrogatio',
    version='1.0.1',
    description='A python library to prompt user '
                'for inputs in a terminal application.',
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'prompt-toolkit>=2.0.8',
        'pygments>=2.3.1',
        'six>=1.12.0'
    ],
    extras_require={
        'yaml':  ['pyyaml>=5',],
        'zxcvbn': ['zxcvbn>=4.4.27'],
        'test':  ['isort', 'flake8', 'ipdb', 'pytest', 'pytest-cov', 'pytest-runner'],
    },
    entry_points={
        'console_scripts': [
            'interrogatio = interrogatio.main:main_interrogatio',
            'dialogus = interrogatio.main:main_dialogus'
        ]
    },
    author='Francesco Faraone',
    author_email='ffaraone@gmail.com',
    url='https://github.com/ffaraone/interrogatio',
    license='BSD 3-Clause',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Terminals'
    ],
    keywords='console input dialog curses prompt',
    include_package_data=True
)
