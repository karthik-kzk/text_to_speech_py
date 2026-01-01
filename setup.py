from setuptools import setup

setup(
    name="tamil-parler-tts",
    version="0.1.0",
    description="Reusable Tamil Text-to-Speech utility using Parler-TTS (AI4Bharat)",
    author="kzk",
    py_modules=["tts"],
    python_requires=">=3.12",
    install_requires=[
        "torch",
        "transformers",
        "parler-tts",
        "soundfile",
    ],
)
