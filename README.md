#Docker image to provision a cluster

*Note if your user is not part of the docker group, run commands with sudo.*

## Set up SSH

See [SSH_README.md](/SSH_README.md/)

## [optional] USE LATEST STABLE AMI

Check [this page](https://coreos.com/os/docs/latest/booting-on-ec2.html) for the HVM ami-xxxxxx id
for your EC2 region.

You can replace the vars->ami value in [ansible/aws_coreos_site.yml](/ansible/aws_coreos_site.yml/)
with this latest id.

## Set all the required variables

```sh
## Get a new etcd token for a new cluster, 5 refers to the number of initial boxes in the cluster:
## `curl https://discovery.etcd.io/new?size=5`
TOKEN_URL=https://discovery.etcd.io/xxxxxx

## Secret used during provision to decrypt keys - get it off your closest buddy!
VAULT_PASS=xxxxxxxx

## AWS API keys, get these off your buddy too
AWS_SECRET_ACCESS_KEY=xxxxxxx
AWS_ACCESS_KEY_ID=xxxxxxxx

# [optional]
SERVICE_DEFINITION_LOCATION=https://raw.githubusercontent.com/Financial-Times/up-service-files/master/services.yaml
# make a unique identifier (you can use this to search your splunk logs as well)
ENVIRONMENT_TAG=xxxx
```

## Run the image
```sh
[sudo] docker run \
    -v user_config.json /user_config.json \
    -v keys.yaml /keys.yaml --env "VAULT_PASS=$VAULT_PASS" \
    --env "TOKEN_URL=$TOKEN_URL" \
    --env "SERVICE_DEFINITION_LOCATION=$SERVICE_DEFINITION_LOCATION" \
    --env "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" \
    --env "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" \
    --env "ENVIRONMENT_TAG=$ENVIRONMENT_TAG" coco/provisioner

