# polly

Use AWS Polly to generate speech from text in the form of mp3 files.

## Prerequisites

- Python 3.6 or higher
- AWS account with Polly access
- AWS credentials configured (via AWS CLI, environment variables, or IAM role)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials (choose one method):
```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

## Usage

### Basic usage with default sample text:
```bash
python polly_tts.py
```

### Custom text:
```bash
python polly_tts.py "Hello, this is my custom text to convert to speech"
```

### Output:
- Creates an MP3 file named `polly_output.mp3` in the current directory

## Features

- Text-to-speech conversion using AWS Polly
- MP3 output format
- Neural voice engine for high-quality audio
- Configurable voice selection
- Error handling for AWS API calls

## Available Voices

The script uses "Joanna" by default, but you can modify the code to use other voices:
- Neural: Joanna, Matthew, Ivy, Kevin, Kimberly, Salli, Joey, Justin, Ruth, Stephen
- Standard: Many additional options available

## Examples

```
python polly_tts.py --profile myprofile --output hello.mp3 --voice Ruth "Hello World"
```

## Open MP3

```
vlc hello.mp3 
```