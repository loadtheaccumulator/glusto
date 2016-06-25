from setuptools import setup

setup(name='glusto',
    version='0.1',
    description='Gluster Object-oriented Python Framework',
    author='Jonathan Holloway',
    author_email='loadtheaccumulator@gmail.com',
    url='http://github.com/loadtheaccumulator/glusto',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Quality Assurance',
        ],
    packages=['glusto', 'tests'],
    entry_points={
        'console_scripts': [
            'glusto = glusto.main:main',
        ]
    },
    install_requires=['plumbum', 'decorator', 'rpyc']
)
