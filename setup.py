"""Setup configuration for mdp_taxi package."""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="mdp_taxi",
    version="2.0.0",
    description="Taxi MDP solver using value iteration with visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MDP Project",
    python_requires=">=3.7",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "pygame>=2.5.0",
        "PyYAML>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "mdp-solve=scripts.solve_mdp:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="mdp reinforcement-learning value-iteration taxi-problem",
)
