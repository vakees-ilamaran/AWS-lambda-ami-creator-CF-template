# AWS-cloudformation-lambda-ami-creator-template
Lambda function to create a image and CF template to deploy the lambda function

## How to Use
Use this below cloudFormation template to deploy this lambda function

Tag an instance with you want to create an image
```
Name: ScheduledBackup
Value: True
```

### IAM roles to be created
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Sid": "Stmt1485904940187",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeTags",
                "ec2:CreateImage",
                "ec2:CreateTags"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
                     ] 
    }


## How to Use CloufFormation Template

#### Install AWS CLI
[Amazon link for installing AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)

#### Configure your CLI
```
[default]
aws_access_key_id = XXXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
region = eu-west-2
```

#### Validate your template
``` 
aws cloudformation validate-template --template-body file://./Cloudformation_Lambda_Deploy.yaml
```

#### Create a stack using your template
``` 
aws cloudformation create-stack --stack-name ec2-test-stack --template-body  file://./Cloudformation_Lambda_Deploy.yaml
```

#### Update your stack in-case of any modification on the template
``` 
aws cloudformation update-stack --stack-name ec2-test-stack --template-body  file://./Cloudformation_Lambda_Deploy.yaml
```
___
## Optional way to update stack
#### You can create a change set and execute it for updating the stack from the cloudformation UI.
```
aws cloudformation create-change-set --stack-name ec2-test-stack --template-body file://./Cloudformation_Lambda_Deploy.yaml --change-set-name port-update --description "updating the lambda function name"
```

Author Information
------------------
[vakees](https://github.com/vakees1424)
