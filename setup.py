from setuptools import setup, find_packages

file = open('README.md', 'r')
long_description = file.read()
file.close()

setup(
    name='gitcode', 
    version='0.1', 
    description='Interact with Git through Python', 
    long_description=long_description, 
    url='https://github.com/WindJackal/gitcode', 
    author='Angus Timothy Olivier', 
    author_email='angusolivier18@gmail.com', 
    license='MIT', 
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers', 
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent', 
        'Programming Language :: Python :: 3', 
        'Topic :: Software Development :: Version Control',
    ], 
    keywords='git version control source development', 
    project_urls={
        'Documentation': 'https://github.com/WindJackal/gitcode/README.md', 
        'Source': 'https://github.com/WindJackal/gitcode', 
        'Tracker': 'https://github.com/WindJackal/gitcode',
    }, 
    packages=find_packages(), 
    python_requires='>=3.5', 
    include_package_data=True,
)