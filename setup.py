from setuptools import setup

setup(name='glusto',
      version='0.2.1',
      author='Jonathan Holloway',
      author_email='loadtheaccumulator@gmail.com',
      description=('A framework of commonly used tools for developing scripts '
                   'in a remote/distributed environment via a single and '
                   'easy-to-access object.'),
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
      install_requires=['plumbum', 'decorator', 'rpyc', 'pytest', 'nose']
      )
