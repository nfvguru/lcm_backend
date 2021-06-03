import falcon
import boto3
from pprint import pprint


class LavaAws:
    def format_instance_output(self, instance):
        ret_val={}
        keys_to_copy =[
            'ImageId',
            'InstanceId',
            'InstanceType',
            'NetworkInterfaces',
            'Tags',
            'State'
        ]
        for key in keys_to_copy:
            if key in instance:
                if key != 'NetworkInterfaces':
                    ret_val[key]=instance[key]
        return ret_val


    def list_instances(self, filtes):
        aws_mgm=boto3.session.Session(profile_name="rad1")
        aws_ec2=aws_mgm.client(service_name='ec2', region_name='us-east-1')
        response=aws_ec2.describe_instances(Filters=filtes)
        my_instances=[]
        for item in response['Reservations']:
            for instance in item['Instances']:
                #pprint(instance)
                #my_instances.append(instance['InstanceId'])
                output_val=self.format_instance_output(instance)
                my_instances.append(output_val)

        res={'instances':my_instances}
        return res
