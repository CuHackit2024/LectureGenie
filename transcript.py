import boto3
import time
import json

REGION = "us-west-2"
SAMPLE_RATE = 16000
BYTES_PER_SAMPLE = 2
CHANNEL_NUMS = 1
CHUNK_SIZE = 1024 * 8
JOB_NAME = "TRANSCRIBE-CUHACKIT2"
S3_BUCKET = "transcibe-cuhackit"


AUDIO_PATH = "/Users/justinsilva/cuhackit/lecturegenie/GMT20231020-103151_Recording_2736x1824.mp4"

#put the audio file in an s3 bucket
s3 = boto3.client('s3')
# with open('test.jpg', 'rb') as data:
#     s3.Bucket('my-bucket').put_object(Key='test.jpg', Body=data)
with open(AUDIO_PATH, 'rb') as data:
    s3.upload_fileobj(data, S3_BUCKET, 'GMT20231020-103151_Recording_2736x1824.mp4')

client = boto3.client('transcribe')

response = client.start_transcription_job(
    TranscriptionJobName=JOB_NAME,
    LanguageCode='en-US',  # Specify the language code appropriate for your audio
    MediaFormat='mp4',  # Specify the format of your audio file
    Media={
        'MediaFileUri': f's3://{S3_BUCKET}/GMT20231020-103151_Recording_2736x1824.mp4'
    },
    OutputBucketName=S3_BUCKET,
    OutputKey='output/transcription.json',
    Settings={
        'ShowSpeakerLabels': True,
        'MaxSpeakerLabels': 2,  # Adjust as needed
        'ChannelIdentification': False  # Change based on your audio file
    }
)

#get the transcript from the job

output_key = "output"


while True:
    status = client.get_transcription_job(TranscriptionJobName=JOB_NAME)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        print(f"Job Status: {status['TranscriptionJob']['TranscriptionJobStatus']}")
        break
    else:
        print("Waiting for transcription job to complete...")
        time.sleep(30)  # Poll every 30 seconds

if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    transcription_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
else:
    print("Transcription job failed.")
    transcription_file_uri = None

if transcription_file_uri:
    # Extract the S3 key from the URI
    output_key = transcription_file_uri.split('/')[-1]
    
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    
    # Download the file
    with open('my_transcription_result.json', 'wb') as f:
        s3.download_fileobj(S3_BUCKET, output_key, f)
        
        print(f"Transcription output downloaded: {f}")

file_path = 'my_transcription_result.json'

# Load the JSON content into a Python dictionary
with open(file_path, 'r') as file:
    transcription_result = json.load(file)

print(transcription_result)