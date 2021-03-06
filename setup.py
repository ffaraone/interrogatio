from setuptools import find_packages, setup

setup(
    name='interrogatio',
    version=__import__('interrogatio').get_version(),
    description='A python library to prompt user for inputs in a terminal application',
    packages=find_packages(),
    install_requires=[
        'prompt-toolkit>=2.0.8', 
        'pygments>=2.3.1',
        'six>=1.12.0'
    ],
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
        'Programming Language :: Python',
        'Topic :: Terminals',
    ],
    keywords='console input dialog curses prompt',
)
