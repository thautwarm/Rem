from setuptools import setup

setup(
    name='remlang',
    version='0.3.1',
    packages=['remlang', 'remlang.compiler', 'remlang.standard'],
    url='https://github.com/thautwarm/Rem',
    license='MIT',
    author='thautwarm',
    author_email='twshere@outlook.com',
    description='rem langauge, which is very comfortable.',
    entry_points={
        'console_scripts': [
            'irem=remlang.intepreter:repl',
            'remlang=remlang.execute:run'
        ]
    },
    platforms='any',
    install_requires=[
        'EBNFParser >= 1.0.5',
        'cytoolz'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython'],
    zip_safe=False)
