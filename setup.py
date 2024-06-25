from setuptools import setup, find_packages

setup(
    name='jrt-green-laser',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'time'
        'serial'
    ],
    author='Samuel Reedy',
    author_email='samreedy7@gmail.com',
    description='A library to use the BA9D Green Laser Module from Chengdu JRT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MAUI65/jrt-green-laser',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)