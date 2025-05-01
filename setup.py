from setuptools import setup, find_packages


setup(
    name="ml_fastapi",
    version="0.1.0",
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    install_requires=[
        "fastapi>=0.115.12",
        "uvicorn>=0.34.2",
        "pydantic>=2.11.4",
        "scikit-learn>=1.6.1",
    ],
    extras_require={
        "dev": [
            "pylint>=3.3.6",
            "pytest>=8.3.5",
            "pytest-cov>=6.1.1",
            "black>=25.1.0",
        ],
    },
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "mlapi=main:app",
        ],
    },
)
