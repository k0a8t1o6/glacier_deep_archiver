import os
import boto3
import hashlib

def initiate_glacier_upload(file_path, part_size):
    glacier = boto3.client('glacier')
    vault_name = os.environ['GLACIER_VAULT_NAME']
    response = glacier.initiate_multipart_upload(
        vaultName=vault_name,
        partSize=str(part_size),
        archiveDescription=file_path,
    )
    return response['uploadId']

def upload_parts(file_path, upload_id, part_size):
    glacier = boto3.client('glacier')
    with open(file_path, 'rb') as f:
        part_number = 1
        while True:
            data = f.read(part_size)
            if not data:
                break
            response = glacier.upload_multipart_part(
                vaultName=os.environ['GLACIER_VAULT_NAME'],
                uploadId=upload_id,
                body=data,
                range='bytes {}-{}/{}'.format(
                    (part_number - 1) * part_size,
                    (part_number - 1) * part_size + len(data) - 1,
                    os.path.getsize(file_path),
                ),
            )
            if not response['checksum']:
                raise Exception('Failed to upload part {}'.format(part_number))
            part_number += 1
    return response

def complete_glacier_upload(file_path, upload_id, response):
    glacier = boto3.client('glacier')
    archive_size = str(os.path.getsize(file_path))
    response = glacier.complete_multipart_upload(
        vaultName=os.environ['GLACIER_VAULT_NAME'],
        uploadId=upload_id,
        archiveSize=archive_size,
        checksum=response['checksum']
    )
    return response['archiveId']

def upload_to_glacier_deep_archive(directory_path, part_size=1024 * 1024 * 128):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            upload_id = initiate_glacier_upload(file_path, part_size)
            try:
                response = upload_parts(file_path, upload_id, part_size)
            except Exception as e:
                print(str(e))
                continue
            archive_id = complete_glacier_upload(file_path, upload_id, response)
            print(f'Uploaded {file_path} to Glacier Deep Archive with archive ID {archive_id}')

if __name__ == '__main__':
    directory_path = input('Enter directory path: ')
    upload_to_glacier_deep_archive(directory_path)
