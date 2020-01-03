from setuptools import setup, find_packages

setup(
    name='siglent',
    version='0.1',
    license='MIT',
    packages=['siglent'],
    description='Waterfall Siglent scope traces',
    author="Eric Waller",
    install_requires=[
        'Click', 'pyqtgraph', 'PyQt5', 'PyOpenGL', 'scipy', 'pyvisa',
    ],
    entry_points={
        'console_scripts': ['siglent=siglent.__main__:main', ], }
)
