"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages


setup(
    name="oo-ops-framework",  # Required
    version="0.1.1",  # Required
    description="运维系统框架",  # Optional
    url="https://github.com/YuBoWe/opsSysFw-dj/",  # Optional
    author="菜鸟wei",  # Optional
    author_email="dededeargo@gmail.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(),  # Required
    python_requires=">=3.8, <4",
    project_urls={  # Optional
        "Bug Reports": "https://github.com/YuBoWe/opsSysFw-dj/issues",
        "Source": "https://github.com/YuBoWe/opsSysFw-dj/",
    },
    data_files=[('', ['requirements'])],
    py_modules=['manage']
)