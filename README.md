# glacier_deep_archiver
Scripts to manage Amazon s3 Glacier service.

As the prerequisite, it is required to create s3 glacier vaults.
```
export AWS_PROFILE=profile_name  //if not default
export GLACIER_VAULT_NAME=vault_name
python3 deep_archiver.py
```

## References
- Amazon s3 Glacier Developer Guide: https://docs.aws.amazon.com/amazonglacier/latest/dev/introduction.html
- Boto3 Glacier: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html