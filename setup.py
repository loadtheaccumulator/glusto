from setuptools import setup

setup(name='glusto',
      version='0.62.2',
      author='Jonathan Holloway',
      author_email='loadtheaccumulator@gmail.com',
      description=('A library of commonly used tools for developing scripts '
                   'in a remote/distributed environment via a single and '
                   'easy-to-access object.'),
      url='http://github.com/loadtheaccumulator/glusto',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Quality Assurance',
        ],
      packages=['glusto'],
      entry_points={
        'console_scripts': [
            'glusto = glusto.main:main',
            ]
                    },
      install_requires=['plumbum', 'rpyc', 'PyYAML', 'jinja2',
                        'pytest', 'nose', 'unittest-xml-reporting']
      )
