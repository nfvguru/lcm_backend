import falcon
import boto3


class LavaAws:

    def list_srvr_vm(self):
        aws_mgm=boto3.session.Session(profile_name="rad1")
        aws_ec2=aws_mgm.client(service_name='ec2', region_name='us-east-1')
        F1={'Name':'tag:Name','Values':['lava_srvr']}
        response=aws_ec2.describe_instances(Filters=[F1])
        srver_instance=[]
        for item in response['Reservations']:
            for instance in item['Instances']:
                srver_instance.append(instance['InstanceId'])
        res={'retcode':srver_instance}
        return res
