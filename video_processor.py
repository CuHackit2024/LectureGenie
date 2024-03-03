import boto3
import streamlit as st
#class that handles the transcription of the video

#a function that transcribes the video

# a function the json returned from the transcribe job and returns all the times as a list

import boto3
import time
import json

class VideoTranscriber:
    def __init__(self, region="us-west-2", s3_bucket="transcibe-cuhackit", job_name_prefix="TRANSCRIBE"):
        self.region = region
        self.s3_bucket = s3_bucket
        self.job_name_prefix = job_name_prefix
        self.s3_client = boto3.client('s3', region_name=region)
        self.transcribe_client = boto3.client('transcribe', region_name=region)

    def upload_video_to_s3(self, file_obj, s3_file_name):
        """Uploads a file-like object to an S3 bucket.

        :param file_obj: File-like object to upload.
        :param s3_file_name: S3 object name where the file will be saved.
        """
        try:
            self.s3_client.upload_fileobj(Fileobj=file_obj, Bucket=self.s3_bucket, Key=s3_file_name)
            print(f"Uploaded to s3://{self.s3_bucket}/{s3_file_name}")
        except Exception as e:
            print(f"Failed to upload file to S3: {e}")


    def start_transcription_job(self, file_name, language_code='en-US', media_format='mp4', max_speaker_labels=2, show_speaker_labels=True):
        job_name = f"{self.job_name_prefix}-{int(time.time())}"
        media_uri = f"s3://{self.s3_bucket}/{file_name}"

        response = self.transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode=language_code,
            MediaFormat=media_format,
            Media={'MediaFileUri': media_uri},
            OutputBucketName=self.s3_bucket,
            OutputKey='output',
            Settings={
                # 'ShowSpeakerLabels': show_speaker_labels,
                # 'MaxSpeakerLabels': max_speaker_labels,
                'ShowAlternatives': True,
                'MaxAlternatives': 2,
                
            }
        )
        

        print(f"Started transcription job: {job_name}")
        return job_name

    def get_transcription_times(self, job_name):
        # Poll for the job to complete
        while True:
            status = self.transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Waiting for transcription job to complete...")
            time.sleep(5)

        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            # Download and process the transcript JSON
            transcript_file = self.s3_client.get_object(Bucket=self.s3_bucket, Key=transcript_file_uri.split('/')[-1])
            #download transcript file into directory
            
            
            transcript_text = json.loads(transcript_file['Body'].read().decode('utf-8'))
            
            segment_details = {}

            for segment in transcript_text['results']['segments']:
                start_time = segment['start_time']
                end_time = segment['end_time']
                transcript = segment['alternatives'][0]['transcript'] if segment['alternatives'] else 'N/A'
                
                # Concatenate start and end times into a single string key
                time_key = f"{start_time}-{end_time}"
                
                # Use the concatenated time string as the key
                segment_details[time_key] = transcript

                print(segment_details)

            print(f'segment_details: {segment_details}')
            return segment_details
        else:
            print("Transcription job failed.")
            return None
