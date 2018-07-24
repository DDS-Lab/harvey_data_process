import time 
import boto3

session = boto3.Session(profile_name='DSSG2018-ddd-team')

client = session.client('ec2')

# starting spot instances

request = client.request_spot_instances(
                SpotPrice= '0.02',
                InstanceCount=1,
                Type='persistent',
                LaunchSpecification={
                    'ImageId': 'ami-e580c79d',
                    'InstanceType': 't2.micro',
                    'SecurityGroupIds': [ "sg-01c4ea7e" ],
                    'KeyName': 'dssg2018-ddd-keypair',
                    'SubnetId':"subnet-972d2ddf" ,
                }
            )


# getting the request description
request_id = request['SpotInstanceRequests'][0]['SpotInstanceRequestId']
request_description = client.describe_spot_instance_requests(SpotInstanceRequestIds=[request_id])

time.sleep(10)


# client.get_waiter(request_description['SpotInstanceRequests'][0]['Status']['Code']=='fulfilled')


# if request_description['SpotInstanceRequests'][0]['Status']['Code']=='fulfilled':
#	print('fullfilled')
#else:
#	print('not fullfiled')


# creating a list of instances associated with the request (maybe I need to update this in case the instances gets restarted)
instance_ids = [print(item) for item in request_description['SpotInstanceRequests']]
print(instance_ids)


# tag all instances
client.create_tags(Resources = instance_ids,Tags = [{'Key':'Name','Value':'spot_gpu'}])
client.create_tags(Resources = instance_ids,Tags = [{'Key':'Project','Value':'dssg2018-ddd'}])
client.create_tags(Resources = instance_ids,Tags = [{'Key':'Email','Value':'vms16@uw.edu'}])

# cancel all instances & the request


# getting the most up to date instance ids
request_description = client.describe_spot_instance_requests(SpotInstanceRequestIds=[request_id])
instance_ids = [item['InstanceId'] for item in request_description['SpotInstanceRequests']]
instance_ids = [print(item) for item in request_description['SpotInstanceRequests']]


# terminate instances
client.terminate_instances(instance_ids)


client.cancel_spot_instance_requests(request_id)
