import os
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
# from pprint import pprint

# Ref:
# {
#     'id': {'key': 'id', 'type': 'str'},
#     'name': {'key': 'name', 'type': 'str'},
#     'type': {'key': 'type', 'type': 'str'},
#     'location': {'key': 'location', 'type': 'str'},
#     'tags': {'key': 'tags', 'type': '{str}'},
#     'plan': {'key': 'plan', 'type': 'Plan'},
#     'hardware_profile': {'key': 'properties.hardwareProfile', 'type': 'HardwareProfile'},
#     'storage_profile': {'key': 'properties.storageProfile', 'type': 'StorageProfile'},
#     'additional_capabilities': {'key': 'properties.additionalCapabilities', 'type': 'AdditionalCapabilities'},
#     'os_profile': {'key': 'properties.osProfile', 'type': 'OSProfile'},
#     'network_profile': {'key': 'properties.networkProfile', 'type': 'NetworkProfile'},
#     'diagnostics_profile': {'key': 'properties.diagnosticsProfile', 'type': 'DiagnosticsProfile'},
#     'availability_set': {'key': 'properties.availabilitySet', 'type': 'SubResource'},
#     'virtual_machine_scale_set': {'key': 'properties.virtualMachineScaleSet', 'type': 'SubResource'},
#     'proximity_placement_group': {'key': 'properties.proximityPlacementGroup', 'type': 'SubResource'},
#     'priority': {'key': 'properties.priority', 'type': 'str'},
#     'eviction_policy': {'key': 'properties.evictionPolicy', 'type': 'str'},
#     'billing_profile': {'key': 'properties.billingProfile', 'type': 'BillingProfile'},
#     'host': {'key': 'properties.host', 'type': 'SubResource'},
#     'provisioning_state': {'key': 'properties.provisioningState', 'type': 'str'},
#     'instance_view': {'key': 'properties.instanceView', 'type': 'VirtualMachineInstanceView'},
#     'license_type': {'key': 'properties.licenseType', 'type': 'str'},
#     'vm_id': {'key': 'properties.vmId', 'type': 'str'},
#     'resources': {'key': 'resources', 'type': '[VirtualMachineExtension]'},
#     'identity': {'key': 'identity', 'type': 'VirtualMachineIdentity'},
#     'zones': {'key': 'zones', 'type': '[str]'},
# }


class LavaAzure:
    def format_instance_output(self, instance):
        # 'ImageId',
        # 'InstanceId',
        # 'InstanceType',
        # 'NetworkInterfaces',
        # 'Tags',
        # 'State'
        ret_val={}
        ret_val['ImageId']=""
        ret_val['InstanceId']=instance.vm_id
        ret_val['InstanceType']=instance.type
        ret_val['Tags']= [{'Key':'Name', 'Value': instance.name}]
        # ret_val['State']={
        #     'Code': instance.instance_view.statuses[1].code,
        #     'Name': instance.instance_view.statuses[1].display_status
        # }
        # ret_val['Tags']=instance.tags
        # ret_val['State']=instance.provisioning_state
        # instance_view.statuses[1].display_status
        # 'Tags': [{'Key':'Name', 'Value': 'amazonVM1'}],
        # 'State': {'Code': '80', 'Name':'running'}}]
        return ret_val


    def list_instances(self, filtes):
        LAVA_SUBS=os.environ['lavans_subs_id']
        LAVA_CLN=os.environ['lavanz_cln_id']
        LAVA_SEC=os.environ['lavans_cln_sec']
        LAVA_TEN=os.environ['lavans_ten_id']
        
        credential = ClientSecretCredential(
            tenant_id=LAVA_TEN,
            client_id=LAVA_CLN,
            client_secret=LAVA_SEC
        )

        compute_client = ComputeManagementClient(
            credential=credential,
            subscription_id=LAVA_SUBS
        )
        my_instances=[]
        for vm in compute_client.virtual_machines.list_all():
            for filter in filtes:
                if bool(filter in vm.name):
                    output_val=self.format_instance_output(vm)
                    vm_state = compute_client.virtual_machines.instance_view(resource_group_name="lavaNew", vm_name=vm.name)
                    power_state = vm_state.statuses[1].display_status
                    # print(power_state.split()[1])
                    output_val['State']= {'Code': '00', 'Name':power_state.split()[1]}
                    my_instances.append(output_val)
        res={'instances':my_instances}
        return res


# my_lc=LavaAzure()
# my_inst=my_lc.list_instances(['lava'])
# print(my_inst)
# def list_virtual_machines():
#     for vm in compute_client.virtual_machines.list_all():
#         if bool('lavaADM' in vm.name):
#            print(vm.name)
#            pprint(vm)
#
#
# # print (LAVA_SEC)
# list_virtual_machines()
