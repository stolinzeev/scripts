import sys
import boto3
import datetime
import time
now = datetime.datetime.now()
now = now.strftime("%d-%m-%Y")

tag_name = 'tag:backupee'
tag_value = 'true'

image_tag_name = 'rotate'
image_tag_value = 'true'

def main(args):


    ec2 = boto3.client('ec2')
## tag backup=true
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']},
                 {'Name': tag_name, 'Values': [tag_value]}])

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

                    imageId = None
                    while imageId == None:
                        images = ec2.describe_images(
                            Filters=[{'Name': 'name', 'Values': [imageName]}])

                        #print(images)
                        for insta in images['Images']:
                            imageId = insta['ImageId']
                            time.sleep(10)
                            print(imageId)

                            response = ec2.create_tags(
                                Resources=[
                                    imageId,
                                ],
                                Tags=[
                                    {
                                        'Key': image_tag_name,
                                        'Value': image_tag_value
                                    },
                                ]
                            )

pass

if __name__ == "__main__":
   main(sys.argv)