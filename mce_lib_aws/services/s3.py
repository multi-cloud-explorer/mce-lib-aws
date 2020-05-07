from ..common import AWSResource, Asset, tags_to_dict, tags_to_list


class Bucket(AWSResource):
    """
    Required IAM actions:
    - s3:PutBucketTagging
    """

    boto_service_name = 's3'
    arn_pattern = 'arn:aws:s3:::{elem[Name]}'

    _cache_locations = {}

    def _listall(self):
        # S3 API returns all the buckets no matter the given region,
        # do some caching and filter on location.
        cls = self.__class__

        response = self.client.list_buckets()
        for bucket in response['Buckets']:
            print('!!! bucket : ', bucket)
            bucket_name = bucket['Name']

            if cls._cache_locations.get(bucket_name):
                response = cls._cache_locations.get(bucket_name)
            else:
                response = self.client.get_bucket_location(Bucket=bucket_name)
                cls._cache_locations[bucket_name] = response

            location = response.get('LocationConstraint')
            if not location:
                location = 'us-east-1'
            elif location == 'EU':
                location = 'eu-west-1'
            
            if location == self.region:
                yield bucket

    def _parse_tags(self, elem, data):
        arn = self._parse_arn(elem)
        return self.get_tags(arn)

    def _parse_name(self, elem, data, tags):
        return elem['Name']

    def get_tags(self, arn):
        bucket_name = arn.split(':')[5]
        try:
            response = self.client.get_bucket_tagging(Bucket=bucket_name)
            tags_dict = tags_to_dict(response['TagSet'])
        except Exception:
            tags_dict = {}
        return tags_dict

    def set_tags(self, arn, tags_dict):
        current_tags_dict = self.get_tags(arn)
        current_tags_list = tags_to_list(current_tags_dict)

        bucket_name = arn.split(':')[5]
        tags_list = tags_to_list(tags_dict)
        self.client.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': current_tags_list + tags_list
            }
        )

    def unset_tags(self, arn, keys):
        current_tags_dict = self.get_tags(arn)

        for key in list(current_tags_dict.keys()):
            if key in keys:
                del current_tags_dict[key]

        bucket_name = arn.split(':')[5]
        tags_list = tags_to_list(current_tags_dict)
        self.client.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': tags_list
            }
        )
