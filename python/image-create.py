import sys
import boto3
import datetime
import time

now = datetime.datetime.now()
now = now.strftime("%d-%m-%Y")

def main(args):


    ec2 = boto3.client('ec2')

##TODO tag backup=true
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']},
                 {'Name': 'tag:backup', 'Values': ['true']}])

    for res in instances['Reservations']:
        for insta in res['Instances']:
            instanceId = insta['InstanceId']
            print(instanceId)
            for tag in insta['Tags']:
                if (tag['Key'] == 'Name'):
                    instanceName = tag['Value']
                    print(instanceName)
                    imageName = instanceName + '-' + now
                    imageName=imageName.replace(' ', '-')
                    imageName = imageName.replace('>', '')
                    print(imageName)
                    response = ec2.create_image(
                        InstanceId=instanceId,
                        Name=imageName,
                        Description=imageName,
                        NoReboot=True
                    )
                    #time.sleep(30)
pass

if __name__ == "__main__":
   main(sys.argv)