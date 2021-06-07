from setuptools import setup


setup(
    name="pygame_orion",
    version="0.0.1",
    description="A game design framework for Pygame 2",
    long_description="Orion is a design framework built atop Pygame 2. "
                     "It is an opinionated selection of development tools"
                     "curated for the needs of my game development projects.",
    keywords=["pygame", "framework", "design"],
    url="https://github.com/krummja/pygame_orion",
    author="Jonathan Crum",
    author_email="crumja4@gmail.com",
    license="MIT",
    packages=[

    ],
    zip_safe=False,
    python_requires=">=3.8.5",
    setup_requires=[],
    install_requires=["pygame>=2.0.0"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ]
)
