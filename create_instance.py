import oci
import os.path
import sys
import oci_config
import json

def get_availability_domain(identity_client, compartment_id):
    list_availability_domains_response = oci.pagination.list_call_get_all_results(
            identity_client.list_availability_domains,
            compartment_id
        )
    availability_domain = list_availability_domains_response.data[0]
    return availability_domain

def get_shape(compute_client, compartment_id, availability_domain):
    list_shapes_response = oci.pagination.list_call_get_all_results(
        compute_client.list_shapes,
        compartment_id,
        availability_domain=availability_domain.name
    )
    shapes = list_shapes_response.data
    if len(shapes) == 0:
        raise RuntimeError('No available shape was found.')

    vm_shapes = list(filter(lambda shape: shape.shape==oci_config.shape_name, shapes))
    if len(vm_shapes) == 0:
        raise RuntimeError('No available VM shape was found.')

    shape = vm_shapes[0]

    print('Found Shape: {}'.format(shape.shape))

    return shape

def get_image(compute, compartment_id, shape):
    list_images_response = oci.pagination.list_call_get_all_results(
        compute.list_images,
        compartment_id,
        operating_system=oci_config.operating_system,
        shape=shape.shape
    )
    images = list_images_response.data
    if len(images) == 0:
        raise RuntimeError('No available image was found.')

    # For demonstration, we just return the first image but for Production code you should have a better
    # way of determining what is needed
    image = images[0]

    print('Found Image: {}'.format(image.id))
    print()

    return image

def get_launch_instance_details(compartment_id, availability_domain, shape, image, subnet_id, ssh_public_key):

    instance_metadata = {
        'ssh_authorized_keys': ssh_public_key,
    }

    instance_metadata['user_data'] = oci_config.user_data

    instance_name = oci_config.instance_name
    instance_source_via_image_details = oci.core.models.InstanceSourceViaImageDetails(
        image_id=image.id
    )
    create_vnic_details = oci.core.models.CreateVnicDetails(
        subnet_id=subnet_id,
        assign_public_ip=True
    )
    
    # Define the shape configuration here
    shape_config = oci.core.models.LaunchInstanceShapeConfigDetails(
        ocpus=1,  # Number of OCPUs
        memory_in_gbs=1,  # Amount of memory in GBs
    )
    
    launch_instance_details = oci.core.models.LaunchInstanceDetails(
        display_name=instance_name,
        compartment_id=compartment_id,
        availability_domain=availability_domain.name,
        shape=shape.shape,
        shape_config=shape_config,
        metadata=instance_metadata,
        source_details=instance_source_via_image_details,
        create_vnic_details=create_vnic_details
    )
    return launch_instance_details

def launch_instance(compute_client_composite_operations, launch_instance_details):
    launch_instance_response = compute_client_composite_operations.launch_instance_and_wait_for_state(
        launch_instance_details,
        wait_for_states=[oci.core.models.Instance.LIFECYCLE_STATE_RUNNING],
    )
    instance = launch_instance_response.data

    print('Launched Instance: {}'.format(instance.id))
    print('{}'.format(instance))
    print()

    return instance

if __name__ == "__main__":
    config = oci.config.from_file("~/.oci/config", "DEFAULT")
    identity_client = oci.identity.IdentityClient(config)
    compute_client = oci.core.ComputeClient(config)
    compute_client_composite_operations = oci.core.ComputeClientCompositeOperations(compute_client)
    compartment_id = oci_config.compartment_id
    
    with open(os.path.expandvars(os.path.expanduser(oci_config.ssh_public_key_path)), mode='r') as file:
        ssh_public_key = file.read()
    
    availability_domain = get_availability_domain(identity_client, compartment_id)
    shape = get_shape(compute_client, compartment_id, availability_domain)
    image = get_image(compute_client, compartment_id, shape)
    subnet_id = oci_config.public_subnet_id
    
    launch_instance_details = get_launch_instance_details(
            compartment_id, availability_domain, shape, image, subnet_id, ssh_public_key
        )

    instance = launch_instance(compute_client_composite_operations, launch_instance_details)
    with open("new_instance.json", "w") as outfile:
        outfile.write(json.dumps(instance))

