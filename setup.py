from setuptools import setup, find_packages

setup(
    name='Flask-PF-Marshmallow-Swagger',
    version='1.0',
    url='https://github.com/problemfighter/flask-pf-marshmallow-swagger',
    license='Apache 2.0',
    author='Touhid Mia',
    author_email='hmtm.cse@gmail.com',
    description='This is Problem Fighter Flask Marshmallow Swagger Extension',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Marshmallow',
        'Apispec',
        'marshmallow-sqlalchemy'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)