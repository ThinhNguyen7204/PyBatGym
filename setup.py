from setuptools import setup, find_packages

setup(
    name="pybatgym",
    version="0.1.0",
    description="Gymnasium environment for BatSim High Performance Computing Simulator",
    author="Google Deepmind Team (Antigravity)",
    packages=find_packages(),
    install_requires=[
        "gymnasium>=0.28.1",
        "numpy>=1.24.0",
        "pyzmq>=25.0.0",
    ],
    extras_require={
        "examples": ["stable_baselines3>=2.0.0"],
        "dev": ["pytest", "mypy", "black"]
    },
    python_requires=">=3.8",
)
