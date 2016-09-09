## About This Project

Project Harbor is an enterprise-class registry server that stores and distributes Docker images. Harbor extends the open source Docker Distribution by adding the functionalities usually required by an enterprise, such as security, identity and management. As an enterprise private registry, Harbor offers better performance and security. Having a registry closer to the build and run environment improves the image transfer efficiency. Harbor supports the setup of multiple registries and has images replicated between them. With Harbor, the images are stored within the private registry, keeping the bits and intellectual properties behind the company firewall. In addition, Harbor offers advanced security features, such as user management, access control and activity auditing.

This project offer a command-line interface to the Harbor API, you can use it to manager your users, projects, repositories, etc.

## Quick Start

#### 1. Get the source code:

On an Internet connected host, Harborclient can be easily got via git:

```sh
git clone https://github.com/int32bit/harborclient
```

#### 2. Setup & Install

Install Harborclient with the following commands. Note that the setup process can take a while.

```sh
sudo pip install -r requirements.txt
sudo python setup.py install
```

#### 3. Verify operation

As the `admin` user, do a login request:

```
$ harbor --os-baseurl http://localhost login --username admin --password Harbor12345
Successfully login, session id: 989a01ccd500a44f9908939dc96822b3
```

## Create harbor client environment scripts

To increase efficiency of client operations, Harborclient supports simple client environment scrips also known as harborrc files.
These scripts typically contain common options for all client, but also support unique options.

### Creating the scripts

Create client environment scripts for the `admin` user. Edit the `~/.admin-harborrc` file and add the following content:

```sh
export HARBOR_USERNAME=admin
export HARBOR_PASSWORD=Harbor12345
export HARBOR_URL=http://localhost
export HARBOR_PROJECT=1
```

Replace `HARBOR_PASSWORD` with your password.


### Using the scripts

To run clients as a specific project and user, you can simply load the associated client environment script prior to running them.

For example:

```
source ~/.admin-harborrc
```

List users:

```sh
$ harbor user-list
+---------+----------+----------------------+--------------+-------------+
| user_id | username |        email         |   realname   |   comment   |
+---------+----------+----------------------+--------------+-------------+
|    3    | int32bit | int32bit@example.com |   int32bit   |      -      |
|    4    |  harbor  |  harbor@example.com  | harbor@12345 | harbor test |
+---------+----------+----------------------+--------------+-------------+
```

## Run in Docker

you can pull from dockerhub as follows:

```sh
docker pull krystism/harborclient
```

Or you can also build yourself on your localhost:

```sh
docker build -t yourname/harborclient .
```

Then run a docker instance as follows:

```
$ docker run \
 -e HARBOR_USERNAME="admin" \
 -e HARBOR_PASSWORD="Harbor12345" \
 -e HARBOR_URL="http://192.168.56.4" \
 --net host --rm krystism/harborclient user-list

+---------+----------+----------------------+--------------+-------------+
| user_id | username |        email         |   realname   |   comment   |
+---------+----------+----------------------+--------------+-------------+
|    3    | int32bit | int32bit@example.com |   int32bit   |      -      |
|    4    |  harbor  |  harbor@example.com  | harbor@12345 | harbor test |
+---------+----------+----------------------+--------------+-------------+
```

You can create an bash alias for simplify input as follows:

```bash
alias harbor='docker run \
 -e HARBOR_USERNAME="admin" \
 -e HARBOR_PASSWORD="Harbor12345" \
 -e HARBOR_URL="http://192.168.56.4" \
 --net host --rm krystism/harborclient'
```
