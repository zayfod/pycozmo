#!/usr/bin/env python
import argparse
import pycozmo

def main():
    parser = argparse.ArgumentParser(
        description="Basic Commands For cozmo_voice_model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--turbo", action="store_true",
        help="Use Chatterbox Turbo model: faster, lower VRAM, and supports "
            "paralinguistic tags in text like [laugh], [cough], [chuckle], [sigh], [gasp]."
    )

    args = parser.parse_args()

    pycozmo.cozmo_voice_model.VoiceClone().load_model(turbo=args.turbo)

    print("\033[32m Downloaded Model! \033[0m")

if __name__ == "__main__":
    main()