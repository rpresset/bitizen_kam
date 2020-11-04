from setuptools import setup

setup(
    name='bitizen_cam',
    entry_points={
    'console_scripts': [
        'bitizen_cam = bitizen_cam:main',
        ],
    }
)
