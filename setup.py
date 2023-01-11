from distutils.core import setup
import setuptools
from setuptools import setup, Extension

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
      name="wireguard-lib",
      packages=setuptools.find_packages(),
      version="0.1.4",
      author="Viktor Gorinskiy",
      author_email="viktor@gorinskiy.ru",
      description="Библиотека для работы с wireguard",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/viktor-gorinskiy/wireguard-lib",
	install_requires=[
            'qrcode==7.3.1'
      ],
	classifiers=[
		"Programming Language :: Python :: 3.6",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)