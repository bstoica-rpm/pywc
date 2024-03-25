from setuptools import setup

setup (
  name='pywc',
  version='1.0.0',
  py_modules=['pywc'],
  python_requires='>=3.6',
  install_requires=[
    'Click>=8.0',
  ],
  entry_points={
    'console_scripts': [
      'pywc=pywc:main',
    ],
  }
)