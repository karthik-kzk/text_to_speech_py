from tts import generate_tamil_tts_from_json

DESCRIPTION = (
        "Mary's voice delivers a slightly expressive and animated speech "
        "with a moderate speed and pitch. The recording is of very high quality, "
        "with the speaker's voice sounding clear and very close up."
    )

generate_tamil_tts_from_json("ott.json","title",DESCRIPTION)
