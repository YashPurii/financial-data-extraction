from setuptools import setup, find_packages

setup(
    name="financial_extractor",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated Financial Data Extraction & Normalization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YashPurii/financial-extractor",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pytesseract",
        "PyPDF2",
        "pillow",
        "speechrecognition",
        "pydub",
        "requests",
        "pandas",
        "sqlite3"
    ],
    entry_points={
        "console_scripts": [
            "finextract=main:run_pipeline",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
