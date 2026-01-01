import os
import json
import torch
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer


def generate_tamil_tts_from_json(json_path):
    """
    Generate Tamil speech audio using Parler-TTS
    Reads `tamil_translated_title` from JSON
    Saves audio files into ./audio folder
    """

    # -----------------------
    # Config
    # -----------------------
    device = "cpu"
    torch.set_num_threads(4)

    MODEL_NAME = "ai4bharat/indic-parler-tts"
    OUTPUT_FOLDER = "audio"

    DESCRIPTION = (
        "Jaya's voice delivers a slightly expressive and animated speech "
        "with a moderate speed and pitch. The recording is of very high quality, "
        "with the speaker's voice sounding clear and very close up."
    )

    # -----------------------
    # Ensure output folder
    # -----------------------
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # -----------------------
    # Load model & tokenizers
    # -----------------------
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        MODEL_NAME
    ).to(device)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    desc_tok = AutoTokenizer.from_pretrained(
        model.config.text_encoder._name_or_path
    )

    # Tokenize description once
    desc_tokens = desc_tok(DESCRIPTION, return_tensors="pt")
    desc_tokens = {k: v.to(device) for k, v in desc_tokens.items()}

    # -----------------------
    # Load JSON
    # -----------------------
    with open(json_path, "r", encoding="utf-8") as f:
        movies = json.load(f)

    if not isinstance(movies, list):
        raise ValueError("JSON root must be a list")

    # -----------------------
    # Generate audio
    # -----------------------
    for movie in movies:
        tamil_text = movie.get("tamil_translated_title", "").strip()
        title = movie.get("title", "audio")

        if not tamil_text:
            print("⚠️ Skipping entry (missing tamil_translated_title)")
            continue

        # Safe filename
        safe_name = (
            title.replace(" ", "_")
                 .replace("/", "")
                 .replace(":", "")
        )

        output_path = os.path.join(OUTPUT_FOLDER, f"{safe_name}.wav")

        print(f"🎙️ Generating → {tamil_text}")
        print(f"💾 Saving to → {output_path}")

        # Tokenize Tamil text
        prompt_tokens = tokenizer(tamil_text, return_tensors="pt")
        prompt_tokens = {k: v.to(device) for k, v in prompt_tokens.items()}

        # Generate audio
        gen = model.generate(
            input_ids=desc_tokens["input_ids"],
            attention_mask=desc_tokens["attention_mask"],
            prompt_input_ids=prompt_tokens["input_ids"],
            prompt_attention_mask=prompt_tokens["attention_mask"]
        )

        # Save audio
        audio = gen.cpu().numpy().squeeze()
        sf.write(output_path, audio, model.config.sampling_rate)

        print("✅ Saved")

    print("🎉 All Tamil audio files saved in ./audio")
