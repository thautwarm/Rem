from setuptools import setup

with open('./README.rst', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='remlang',
    long_description=readme,
    version='0.4',
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
        'toolz',
        'EBNFParser >= 2.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython'],
    zip_safe=False)
