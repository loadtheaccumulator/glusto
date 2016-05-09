from setuptools import setup

setup(name='glusto',
    version='0.1.0',
    description='Gluster Object-oriented Framework',
    author='Jonathan Holloway',
    author_email='loadtheaccumulator@gmail.com',
    url='http://github.com/loadtheaccumulator/glusto',
    packages=['glusto', 'tests'],
    entry_points={
        'console_scripts': [
            'glusto = glusto.main:main',
        ]
    },
    install_requires=['plumbum']
)
