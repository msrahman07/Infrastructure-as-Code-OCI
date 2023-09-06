# Oracle Cloud Infrastructure Compute Instance Provisioning

This guide explains how to provision a compute instance in Oracle Cloud Infrastructure (OCI) using Python scripts and the OCI Python SDK. The provided Python script (`create_instance.py`) automates the process of launching a compute instance.

## Prerequisites

Before you begin, ensure you have the following prerequisites:

1. **Install OCI Python SDK:**

   Install the Oracle Cloud Infrastructure Python SDK on your local machine. Follow the instructions in the official [installation guide](https://docs.oracle.com/en-us/iaas/tools/python/2.111.0/installation.html).

2. **Generate API Key and Configuration File:**

   Generate an API key and create a configuration file (`~/.oci/config`) to authenticate with OCI. Refer to the following resources for guidance:

   - [Generate API Key](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm#apisigningkey_topic_How_to_Generate_an_API_Signing_Key_Console)
   - [Configure `~/.oci/config`](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm)

3. **Define Configuration Variables:**

   In the `oci_config.py` file (located in the same folder as `create_instance.py`), define the following variables:

   - `compartment_id`: Your designated compartment ID in your tenancy.
   - `ssh_public_key_path`: Path to your RSA public key for SSH communication with the instance.
   - `shape_name`: Name of the desired shape for the compute instance.
   - `operating_system_version`: The OS version you want to use.
   - `public_subnet_id`: Public subnet ID from your Virtual Cloud Network (VCN).
   - `instance_name`: Set a name for your compute instance.

## `create_instance.py` Code Description

Below is a description of the functions and code in `create_instance.py`:

1. `config = oci.config.from_file("~/.oci/config", "DEFAULT")`: Creates an account configuration from `~/.oci/config`.

2. `identity_client = oci.identity.IdentityClient(config)`: Generates an identity client for working with OCI's identity and access management.

3. `compute_client = oci.core.ComputeClient(config)`: Creates a compute client for interacting with compute instances in OCI.

4. `compute_client_composite_operations = oci.core.ComputeClientCompositeOperations(compute_client)`: Creates a compute client composite to perform composite operations.

5. `compartment_id = oci_config.compartment_id`: Retrieves the compartment ID specified in `oci_config.py`.

6. `get_availability_domain(identity_client, compartment_id)`: Retrieves a list of all available domains in your tenancy and selects the first one.

7. `get_shape(compute_client, compartment_id, availability_domain)`: Retrieves a list of available shapes and selects one based on the shape name defined in `oci_config.py`.

8. `get_image(compute, compartment_id, shape)`: Retrieves a list of available images, selects an image based on the specified OS and version.

9. `get_launch_instance_details(compartment_id, availability_domain, shape, image, subnet_id, ssh_public_key)`: Generates instance launch details and metadata based on provided arguments.

10. `launch_instance(compute_client_composite_operations, launch_instance_details)`: Creates an OCI compute instance based on launch details and waits for the instance to reach the 'RUNNING' state.

## Running the Script

To provision a compute instance, follow these steps:

1. **Install Dependencies:**

   Install the required dependencies using pip:

   ```bash
   pip install oci
2. **Run the Script:**
   python create_instance.py

## Customization
You can customize the script further based on your requirements, such as adding additional metadata, customizing the shape configuration, or specifying a different OS image.
