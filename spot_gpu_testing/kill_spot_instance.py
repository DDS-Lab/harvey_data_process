# kill all spot instances by user DSSG2018-ddd-team


import boto3

session = boto3.Session(profile_name='DSSG2018-ddd-team')

client = session.client('ec2', region_name='us-west-2')

request_description = client.describe_spot_instance_requests()

instance_ids = [item['InstanceId'] for item in
                request_description['SpotInstanceRequests']]

request_ids = [item['SpotInstanceRequestId'] for item in
               request_description['SpotInstanceRequests']]

print(request_ids)

print(instance_ids)

client.terminate_instances(InstanceIds=instance_ids)

client.cancel_spot_instance_requests(SpotInstanceRequestIds=request_ids)

# for request in requests['SpotInstanceRequests']:
# 	print(request['InstanceId'])
# 	instance_ids = [item['InstanceId'] for item in request]
# 	print(instance_ids)
