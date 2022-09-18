from setuptools import setup

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name="robot_descriptions_cpp",
    version="1.0.0",
    description="UA package to use robot_descriptions.py with C++",
    license="Apache 2.0",
    author="Sotaro Katayama",
    url="https://github.com/mayataka/robot_descriptions_cpp",
    packages=["robot_descriptions_cpp"],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
)