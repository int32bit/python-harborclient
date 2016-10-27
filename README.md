[中文文档](./README.zh.md)

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

```
$ harbor user-list
+---------+----------+----------------------+--------------+-------------+
| user_id | username |        email         |   realname   |   comment   |
+---------+----------+----------------------+--------------+-------------+
|    3    | int32bit | int32bit@example.com |   int32bit   |      -      |
|    4    |  harbor  |  harbor@example.com  | harbor@12345 | harbor test |
+---------+----------+----------------------+--------------+-------------+
```

## Run in Docker

You can pull from Dockerhub directly:

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

You can create an bash alias for simplify input:

```bash
alias harbor='docker run \
 -e HARBOR_USERNAME="admin" \
 -e HARBOR_PASSWORD="Harbor12345" \
 -e HARBOR_URL="http://192.168.56.4" \
 --net host --rm krystism/harborclient'
```

Then run as a simpler way:

```
$ harbor user-list
+---------+----------+----------------------+--------------+-------------+
| user_id | username |        email         |   realname   |   comment   |
+---------+----------+----------------------+--------------+-------------+
|    3    | int32bit | int32bit@example.com |   int32bit   |      -      |
|    4    |  harbor  |  harbor@example.com  | harbor@12345 | harbor test |
+---------+----------+----------------------+--------------+-------------+
```

## Usage examples

Get top 5 accessed repositories:

```
$ harbor top
+----------------+-------+
|      name      | count |
+----------------+-------+
| library/ubuntu |   129 |
| int32bit/harbor|   24  |
| library/python |   21  |
| library/centos |   10  |
| int32bit/qrcode|   2   |
+----------------+-------+
```

Get current user of statistics data:

```
$ harbor statistics
+----------------------+-------+
| Property             | Value |
+----------------------+-------+
| my_project_count     | 3     |
| my_repo_count        | 1     |
| public_project_count | 3     |
| public_repo_count    | 1     |
| total_project_count  | 3     |
| total_repo_count     | 1     |
+----------------------+-------+
```

Show details about the given repository with `--debug` option:

```
$ harbor --debug show ubuntu:14.04
DEBUG (client:282) Successfully login, session id: 82591b568920b4a4f2c36ca1cac4795f
REQ: curl -g -i 'http://192.168.56.4/api/repositories/manifests?repo_name=library/ubuntu&tag=14.04' -X GET -H "Accept: application/json" -H "User-Agent: python-harborclient" -b "beegosessionID: 82591b568920b4a4f2c36ca1cac4795f"
RESP: [200] {'Date': 'Fri, 09 Sep 2016 13:40:02 GMT', 'Content-Length': '320', 'Content-Type': 'application/json; charset=utf-8', 'Connection': 'keep-alive', 'Server': 'nginx/1.9.15'}
RESP BODY: {"Parent": "0e23078ccd338d08cf033f6a300f4dce86a95381c4a9a4beed6cd5a460645ee1", "Author": "", "Created": "2016-05-03T23:11:04.403014677Z", "Docker Version": "", "Duration Days": "128 days", "Architecture": "amd64", "OS": "linux", "Id": "06cc1800c7a47f86127b01cbc13874a4dc8f0bbbe0b45e4a9d4374f13944fe25"}

+----------------+------------------------------------------------------------------+
| Property       | Value                                                            |
+----------------+------------------------------------------------------------------+
| Architecture   | amd64                                                            |
| Author         |                                                                  |
| Created        | 2016-05-03T23:11:04.403014677Z                                   |
| Docker Version |                                                                  |
| Duration Days  | 128 days                                                         |
| Id             | 06cc1800c7a47f86127b01cbc13874a4dc8f0bbbe0b45e4a9d4374f13944fe25 |
| OS             | linux                                                            |
| Parent         | 0e23078ccd338d08cf033f6a300f4dce86a95381c4a9a4beed6cd5a460645ee1 |
+----------------+------------------------------------------------------------------+
```

Print call timing info with `--timings` option:

```
$ harbor --timings list
+--------------+----------------+-------+---------+--------------+-------+
|      Id      |      Name      |  Tag  | Project | Architecture |   OS  |
+--------------+----------------+-------+---------+--------------+-------+
| 06cc1800c7a4 | library/ubuntu | 14.04 |    1    |    amd64     | linux |
+--------------+----------------+-------+--------+---------+-------------+
+----------------------------------------------------------------+------------------+
| url                                                            | seconds          |
+----------------------------------------------------------------+------------------+
| GET /repositories?project_id=1                                 | 0.00539398193359 |
| GET /repositories/tags?repo_name=library/ubuntu                | 0.0393018722534  |
| GET /repositories/manifests?repo_name=library/ubuntu&tag=14.04 | 0.0534088611603  |
| Total                                                          | 0.0981047153473  |
+----------------------------------------------------------------+------------------+
Total: 0.0981047153473 seconds
```

See `harbor help` for more usage info.

## Issues

1. Can't show `admin` user info with name, but `id` work.
2. Delete one user, then create a new user with same email will always fail.
3. Can't delete a project.

## TODO

- [ ] Delete Image
- [ ] Upload Image
- [ ] Create Project
- [ ] ...

## Licensing

HarborClient is licensed under the MIT License, Version 2.0. See [LICENSE](./LICENSE) for the full license text.
