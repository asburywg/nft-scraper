import json
import boto3

from common.operations import get_date

client = boto3.client('s3')


def s3_put_json(data, bucket, filename, prefix=None):
    client.put_object(Body=json.dumps(data), ContentType="application/json", Bucket=bucket,
                      Key=f'{prefix}/{filename}' if prefix else filename)


def s3_read_json(bucket, filename, prefix=None):
    return json.loads(client.get_object(Bucket=bucket, Key=f'{prefix}/{filename}' if prefix else filename)["Body"].read().decode())


def generate_s3_path(prefix, filename):
    return f"{prefix}/{get_date()}/{filename}"


def get_prefix_dates(bucket, prefix):
    response = client.list_objects(Bucket=bucket, Prefix=f"{prefix}/", Delimiter='/').get('CommonPrefixes')
    if not response:
        return []
    return [x.get('Prefix').split('/')[1] for x in response]