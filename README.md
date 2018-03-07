# DevOps Tool Provisioner (DTP)

[![standard-readme compliant](https://img.shields.io/badge/devops-cloud%20provisioning-green.svg)](https://github.com/stelligent/dtp)

> Introducing a new way of using DevOps tools in the cloud

DTP is a tool that simplifies provisioning a virtual machine using any of the following virtualization providers: AWS, GCE, Azure, VirtualBox (At the moment, only AWS has been implemented) and also automatically install and configure one or more standard DevOps tools and also sync files between your local machine and the vm.

This tool directly calls the API of the various backend providers directly, removing any middleman dependencies.

This provides system admins, developers, QAs and other cloud curious individuals to quickly get started on any of the supported cloud providers.

The following tools are currently available:

* cfengine-hub
* chef-client
* chef-server
* docker
* gerrit
* jenkins
* python-dev-env
* redmine
* ruby-dev-env

The tools library is expected to grow as users can submit the configurations of their tools of choice for merge into DTP.

## Table of Contents

- [Features](#feature)
- [Install](#install)
- [Usage](#usage)
- [Examples](#examples)
- [Maintainers](#maintainers)
- [Contribute](#contribute)
- [License](#license)

## Features

* Create VMs running Ubuntu, CentOS, AmazonLinux, RHEL, SUSE or Windows Server
* Specify list of local directories to sync (two-way sync) with VM
* Specify list of tools to be configured on VM at start up
* Define default configuration template containing default provider to provision new VMs not having a configuration file
* Easily create, start, stop, destroy, list, sync with VM
* Manage VMs using simple CLI commands and a easy-to-read configuration file

> For EC2 Instances
* Choose machine type, availability zone, number of vms to provision
* Specify ports to open up

## Install

This project uses [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/); it has been tested on [python 2.7](https://www.python.org/downloads/). Go check them out if you don't have them locally installed.

Also using [virtualenv](https://virtualenv.pypa.io/en/stable/) is preferred to avoid permission issues installing the package dependencies

```sh
# Install virtualenv
$ pip install virtualenv
# Create virtual environment ENV
$ virtualenv ENV
# Activate ENV
$ cd ENV
$ source bin/active
# FYI: To deactivate ENV, run
$ deactivate
```

> Install with pip

```sh
$ pip install dtp
```

> Clone source repo

```sh
$ git clone git@github.com:stelligent/dtp.git
$ cd dtp
# Install
$ python setup.py install
# Try out without installing
$ python -m dtp.dtp
```

## Usage

First create a default configuration file to use for provisioning new VMS when a config file is not defined for the VM. All configurations files should be stored in your home directory. The default configuration should be named dtp_default.cfg

### [Sample configuration file](sample/sample_configuration.cfg)

```sh
[resource]
provider = <aws|azure|docker|gce|vagrant>

[aws]
key_name = <my_key_pair_name>
key_file_location = /tmp/kfl.pem
access_key = <aws_access_key>
secret_key = <aws_secret_key>
platform = <linux|windows>
os_name = <AmazonLinux|Suse|Ubuntu|RHEL|CentOS|Server 2016|Server 2016 R2|Server 2012|Server 2008 R2>
machine_type = <t2.micro|other_machine_types>
az = <us-east-1a|other_availability_zones>
ports = [22,80,...]
local_sync_directory = [/tmp/junk,/home/cloud_user/git/projecta]

[azure]
...

[docker]
...

[gce]
...

[vagrant]
...

[services]
services = [cfengine,jenkins,redmine,...]
```

Once you've created the default configuration file in your home directory

```sh
$ dtp -h
usage: dtp <action> <name>

positional arguments:
  {create,destroy,halt,info,list,login,pull,push,start,status}
                        action required
  name                  Name of resource to create, matching config file

optional arguments:
  -h, --help            show this help message and exit
  --debug, -d, -D       Set log level to debug
```
>

## Examples

* Create a new VM

```sh
$ dtp create new_vm
```

* Get VM status

```sh
$ dtp status new_vm
```

* Start previously stopped VM

```sh
$ dtp start new_vm
```

* Stop running VM

```sh
$ dtp stop new_vm
```

* Destroy a VM, this deletes VM and associated data; be careful running this

```sh
$ dtp destroy new_vm
```

* Sync data from local machine to VM based on local_sync_directory

```sh
$ dtp push new_vm
```

* Sync files from VM to local machine based on local_sync_directory

```sh
$ dtp pull new_vm
```

* List of available VMs and status

```sh
$ dtp list vms|instances
```

* List available DevOps tools that can be configured on VMs

```sh
$ dtp list  tools
```

## Maintainers

[@mayoralade](https://github.com/mayoralade).

## Contribute

DTP follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.

## License

[MIT](LICENSE)
