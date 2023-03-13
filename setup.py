from setuptools import setup, find_namespace_packages

setup(
    name='HW_07_clean_folder',
    version='1.0.0',
    description='Package with scripts for folders handling and sorting',
    url='https://github.com/DenysPhV/HW_07_clean_folder',
    author='Denys Filichkin',
    author_email='philichkindenis1@gmail.com',
    license='MIT',
     classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['HW_07_clean_folder=HW_07_clean_folder.clean:main_script']}
)