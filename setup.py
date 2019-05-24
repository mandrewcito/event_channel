import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="event_channel",
    version="0.1.0",
    author="mandrewcito",
    author_email="anbaalo@gmail.com",
    description="Pub sub implementation",
    keywords="publish subscribe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mandrewcito/event_channel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)