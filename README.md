# threatstack-to-splunk
Takes a Threat Stack web hook request and add an event to Splunk.

**NOTE: This code is provided as an example and without support for creating services that use Threat Stack webhooks to perform actions within an environment.**

## Deployment
This service can be deployed to AWS running on Lambda behind AWS API gateway by clicking "Launch Stack".
[![Launch CloudFormation
Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=threatstack-to-splunk&templateURL=https://s3.amazonaws.com/straycat-dhs-org-straycat-lamba-deploys/threatstack-to-splunk.json)

## API
### POST https://_{host}_/threatstack-to-splunk/api/v1/splunk/event
Post a JSON doc from Threat Stack and record an event in Splunk.  JSON doc will be in the following format.  __NOTE__: A webhook may contain multiple alerts but this service will store each one individually.
```
{
  "alerts": [
    {
      "id": "<alert ID>",
      "title": "<alert title / description>",
      "created_at": <time in milliseconds from epoch UTC>,
      "severity": <severity value>,
      "organization_id": "<alphanumeric organization ID>",
      "server_or_region": "<name of host in Threat Stack platform>",
      "source": "<source type>"
    }
  [
}
```

## Standalone Setup / Build / Deployment
### Setup
Setup will need to be performed for both this service and in Threat Stack.

Set the following environmental variables:
```
$ export SPLUNK_HEC_TOKEN=<API token>
$ export SPLUNK_HOST=<hostname>
$ export THREATSTACK_API_KEY=<Threat Stack API key>
```

Create and initialize Python virtualenv using virtualenvwrapper
```
mkvirtualenv threatstack-to-splunk
pip install -r requirements.txt
```

__NOTE:__ If Running on OS X you will need extra packages to work around issues with Python and SSL. OS X usage should be for development only.
```
pip install -r requirements.osx.txt
```

To launch the service:
```
gunicorn -c gunicorn.conf.py threatstack-to-splunk
```

If performing debugging you may wish to run the app directly instead of via Gunicorn:
```
python threatstack-to-splunk.py
```

### Build
This service uses [Chef Habitat](http://www.habitat.sh) to build deployable packages.  Habitat supports the following package formats natively:
* Habitat package (.hart)
* tar
* docker
* aci
* mesos

See the following resources for getting started with Habitat.
* https://www.habitat.sh/docs/overview/
* https://www.habitat.sh/tutorial/

Building packages:
```
# Builds Habitat .hart package
$ hab pkg build build/

# Export a Docker container
$ hab pkg export docker <your_docker_org>/threatstack-to-splunk

# Export a tarball with habitat runtime. (optional)
$ hab pkg export tar tmclaugh/threatstack-to-splunk
```

Building in Hab studio (OS X):
```
$ hab studio enter
[1][default:/src:0]# cd build/

# Builds Habitat .hart package
[2][default:/src/build:0]# build

# Export a Docker container. (optional)
[3][default:/src/build:0]# hab pkg export docker <your_docker_org>/threatstack-to-splunk

# Export a tarball with habitat runtime. (optional)
[3][default:/src/build:0]# hab pkg export tar tmclaugh/threatstack-to-splunk
```

#### Starting service.
If you’re using Docker then follow your typical Docker container deployment steps.  If you’re using a native Habitat package or Habitat tarball then do the following.

* Habitat native package.  (Requires installing Habitat on host.)
```
$ sudo hab start tmclaugh-threatstack-to-splunk-{version}-x86_64-linux.hart
```

* Habitat tarball.  (Contains Habitat with it.)
```
$ sudo tar zxvf {package}.tar.gz -C /
$ sudo /hab/bin/hab tmclaugh/threatstack-to-splunk
```

