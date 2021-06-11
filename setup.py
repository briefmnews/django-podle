from setuptools import setup

setup(
    name="django-podle",
    version="0.1.0",
    description="Integration with Podle.io podcast app",
    url="https://github.com/briefmnews/django-podle",
    author="Brief.me",
    author_email="tech@brief.me",
    license="MIT",
    packages=["podle", "podle.migrations", "podle.signals"],
    python_requires=">=3.7",
    install_requires=[
        "Django>=2.2",
        "djangorestframework>=3",
        "requests>=2",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    zip_safe=False,
)
