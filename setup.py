from setuptools import setup

setup(
    name="tamil-parler-tts",
    version="0.1.0",
    description="Reusable Tamil Text-to-Speech utility using Parler-TTS (AI4Bharat)",
    author="kzk",
    py_modules=["tts"],
    python_requires=">=3.12",
    install_requires=[
        "torch==2.9.1",
        "transformers==4.46.1",
        "parler-tts==0.2.2",
        "soundfile==0.13.1",
    ],
)
