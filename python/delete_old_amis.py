import sys
import boto3
import datetime


now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %I:%M:%S")
now = datetime.datetime.strptime(now, "%Y-%m-%d %I:%M:%S")
#print(now)

last_days = 90
tag_name = 'tag:rotate'
tag_value = 'true'

def main(args):
    ec2 = boto3.client('ec2')


## tag rotate=true
    images = ec2.describe_images(
         Filters=[{'Name': tag_name, 'Values': [tag_value]}])

    print(images)
    for insta in images['Images']:
        imageId = insta['ImageId']
        #print(imageId)
        image_date = insta['CreationDate']
        #print(image_date[:10])
        f = image_date[:10]
        f = datetime.datetime.strptime(f, "%Y-%m-%d")
        #print(f)
        d = (now - f).days
        #print(d)
        if d > last_days:
            print('Deleting' ' ' + imageId)
            responce = ec2.deregister_image(
                ImageId=imageId
            )
            print(imageId + ' ' 'Deleted')
        else:
            print('Nothing to delete')




pass

if __name__ == "__main__":
   main(sys.argv)