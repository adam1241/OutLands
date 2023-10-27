from setuptools import setup, find_packages
setup(
    name="right-left",
    version="0.1",
    packages=find_packages(),
    install_requires=["pygame"],
    description="My Python package",
    author="3bass",
    author_email="your@email.com",
    url="",
    entrypoints={
        'console_scripts': [
            'hello-worlds'
        ],
        },
)