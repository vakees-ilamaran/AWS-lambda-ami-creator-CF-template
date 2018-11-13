from __future__ import print_function
import boto3
import logging
import time
 
current_session = boto3.session.Session()
current_region = current_session.region_name
logger = logging.getLogger()
logger.setLevel(logging.INFO)
        
#create a client connection to ec2
ec2_client = boto3.client('ec2', current_region)

# used to evaluate if any returned structures are empty
def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True
            
            
def get_instances_to_backup(ec2, server_name):
    
    # This function creates a dict of ec2 instances that have
    # a ScheduledBackup tag set to "true"
    
    #print("Looking up instance to backup")
    try:
        if server_name:
            print("Looking up server to image.")
            response = ec2_client.describe_instances(
                Filters=[{'Name':'tag:Name', 'Values': [server_name]}
                    ])
    
        else:
            print("Finding serves with ScheduledBackup tag to image.")
            response = ec2_client.describe_instances(
            Filters=[{'Name':'instance-state-name', 'Values': ['running']},
                        {'Name': 'tag:ScheduledBackup','Values':['true']}
                    ])
        
        #see if the response is empty
        if is_empty(response["Reservations"]):
            raise Exception('No instances were returned. Please make sure that there is a tag ScheduledBackup with a value of true')
        else:
            return response   
        
    
    except Exception as e:
        # Print to the console if there is an error
        print("get_instances_to_backup error: " + str(e)) 
        exit()
            
def create_image(ec2, image_type):
    
    print("Started creating image")
    timestamp = time.strftime('-' + image_type + '-%H%M%b%d%Y')
    
    try:
        for reservation in ec2["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                image_name = instance_id + timestamp
                
                #Add the ServerName Tag to the server
                for tag in instance["Tags"]:
                    if tag["Key"] == "Name":
                        server_name= tag["Value"]
                
                image_name = server_name + "-" + image_name
                
                # for debug purposes and test loop
                # print(image_name)
                
                #create the image
                response = ec2_client.create_image(InstanceId=instance_id,Name=image_name)
                
                print("Created image with id: " + response["ImageId"])
                create_tags_for_image(response, server_name, timestamp, instance_id)
                
                
                
    except Exception as e:
        print("create_image error: " + str(e)) 
    
    
def create_tags_for_image(image, server_name, timestamp, instance_id):
    
    #this function adds a Name tag to the created image
    
    ec2 = boto3.resource('ec2')
    ec2_image = ec2.Image(image["ImageId"])
    
    name_tag = server_name +  timestamp
    print("Adding Name tag " + name_tag + " to image")
    
    ec2_image.create_tags(
        Tags=[
        {
            'Key': 'Name',
            'Value': name_tag,
            'Key': 'instanceId',
            'Value': instance_id
        },
        ]
    )
    
 
def lambda_handler(event, context):
    
    try:
        if event["server_name"]:
            print("Server name passed. Creating image of specific server.")
            server_name = event["server_name"]
            image_type = "called"
            #exit()
    except Exception as e:
        server_name = ""
        image_type = "auto"
        print("Starting scheduled image creation.")
        
    
    try:
        #get a list of instances with tag ScheduledBackup set to "true"       
        instances = get_instances_to_backup(ec2_client, server_name)
        
        if instances == "Fail":
            raise Exception("No instances were returned.")
    
        # create images
        create_image(instances, image_type)
        
        return True
    except Exception as e:
        print("lambda_handler error: "+ str(e))
        return False

            
lambda_handler("", "")
