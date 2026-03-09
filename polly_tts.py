#!/usr/bin/env python3
"""
AWS Polly Text-to-Speech Script
Converts text to speech using AWS Polly and saves as MP3 file.
"""

import boto3
from botocore.exceptions import BotoCoreError, ClientError
import sys
import argparse
from pydub import AudioSegment
from io import BytesIO


def text_to_speech(text, output_file="output.mp3", voice_id="Joanna", engine="neural", aws_profile=None, volume_decrease=0):
    """
    Convert text to speech using AWS Polly and save as MP3.

    Args:
        text (str): The text to convert to speech
        output_file (str): Output filename (default: output.mp3)
        voice_id (str): AWS Polly voice ID (default: Joanna)
        engine (str): Engine type - 'neural' or 'standard' (default: neural)
        aws_profile (str): AWS profile name to use (default: None, uses default profile)
        volume_decrease (float): Volume decrease in dB (default: 0, no change)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create a Polly client with optional profile
        if aws_profile:
            session = boto3.Session(profile_name=aws_profile)
            polly_client = session.client('polly')
        else:
            polly_client = boto3.client('polly')

        print(f"Converting text to speech using voice '{voice_id}'...")

        # Request speech synthesis
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine=engine
        )

        # Access the audio stream from the response
        if "AudioStream" in response:
            # Read the audio stream
            audio_data = response['AudioStream'].read()

            # Apply volume adjustment if requested
            if volume_decrease != 0:
                print(f"Adjusting volume by {volume_decrease} dB...")
                # Load audio into pydub
                audio = AudioSegment.from_file(BytesIO(audio_data), format="mp3")
                # Decrease volume (negative value decreases, positive increases)
                audio = audio - volume_decrease
                # Export to file
                audio.export(output_file, format="mp3")
            else:
                # Write the audio stream directly to file
                with open(output_file, 'wb') as file:
                    file.write(audio_data)

            print(f"✓ Speech successfully saved to '{output_file}'")
            return True
        else:
            print("✗ Could not retrieve audio stream from response")
            return False

    except (BotoCoreError, ClientError) as error:
        print(f"✗ Error occurred: {error}")
        return False


def main():
    """Main function to demonstrate usage."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Convert text to speech using AWS Polly',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python polly_tts.py "Hello world"
  python polly_tts.py --file input.txt
  python polly_tts.py --profile myprofile "Hello world"
  python polly_tts.py --voice Matthew --output speech.mp3 "Hello world"
  python polly_tts.py --volume 5 "Hello world"  # Decrease volume by 5 dB
  python polly_tts.py --volume -3 "Hello world"  # Increase volume by 3 dB
        """
    )

    parser.add_argument('text', nargs='*', help='Text to convert to speech')
    parser.add_argument('--file', '-f', help='Text file to read as input')
    parser.add_argument('--profile', '-p', help='AWS profile name to use')
    parser.add_argument('--voice', '-v', default='Joanna', help='Voice ID (default: Joanna)')
    parser.add_argument('--output', '-o', default='polly_output.mp3', help='Output filename (default: polly_output.mp3)')
    parser.add_argument('--engine', '-e', choices=['neural', 'standard', 'generative'], default='neural',
                        help='Engine type: neural, standard, or generative (default: neural)')
    parser.add_argument('--volume', type=float, default=0,
                        help='Volume decrease in dB (positive values decrease, negative increase, default: 0)')

    args = parser.parse_args()

    # Determine input text
    if args.file:
        try:
            with open(args.file, 'r') as f:
                text = f.read()
        except OSError as e:
            print(f"✗ Could not read file '{args.file}': {e}")
            sys.exit(1)
    elif args.text:
        text = ' '.join(args.text)
    else:
        parser.error("provide text as argument or use --file to specify a text file")

    # Convert text to speech
    success = text_to_speech(
        text=text,
        output_file=args.output,
        voice_id=args.voice,
        engine=args.engine,
        aws_profile=args.profile,
        volume_decrease=args.volume
    )

    if success:
        print("\nAvailable voices include:")
        print("  Neural: Joanna, Matthew, Ivy, Kevin, Kimberly, Salli, Joey, Justin, Ruth, Stephen")
        print("  Generative: Ruth, Stephen, Matthew")
        print("  Standard: Many more options available")
        print("\nNote: Generative engine is optimized for long-form content")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
