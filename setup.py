from setuptools import setup, find_packages

setup(
    name="ai-os",
    version="0.1.0",
    description="Portable Multi-User Live USB Agentic Operating System",
    author="AI-OS Core Team",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.110.0",
        "uvicorn>=0.28.0",
        "websockets>=12.0",
        "jinja2>=3.1.3",
        "pydantic>=2.6.0",
        "cryptography>=42.0.0",
        "psutil>=5.9.8",
        "rich>=13.7.0"
    ],
    entry_points={
        "console_scripts": [
            "aios=src.ui.cli:main",
            "aios-server=src.ui.server:run_server",
            "aios-updater=src.updater.ota_manager:main"
        ]
    }
)
