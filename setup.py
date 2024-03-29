from setuptools import setup

setup(
    name="android-duplicated-images-detector",
    version="1.0.0",
    author="lijiankun24",
    author_email="jiankunli24@gmail.com",
    description="A Python library to detect duplicated images in android apk.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/WEIHAITONG1/better-youtubedl",
    packages=[],
    namespace_packages=[],
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Multimedia :: Video',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'Pillow',
    ],
    zip_safe=True,
)
