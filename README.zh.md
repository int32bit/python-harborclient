[English](./README.md)

## 1 关于Harbor？

Harbor是由VMware中国研发团队负责开发的开源企业级Registry项目，项目地址为`https://github.com/vmware/harbor`，该项目发布5个多月以来，深受用户喜爱，在GitHub获得了1000多个点赞星星和200多个Forks。

Harbor是一个用于存储和分发Docker镜像的企业级Registry服务器，通过添加一些企业必需的功能特性，例如安全、标识和管理等，扩展了开源Docker Distribution，提供了:

* 基于角色的访问控制：用户和存储库是通过“项目”关联，同时用户对同一“项目”下镜像拥有不同访问权限。
* 镜像远程复制（同步）：镜像可以在多个注册表之间复制（同步）。支持负载均衡，高可用性，混合云及多种云的情况。
* 图形管理界面：用户能够快捷浏览、搜索存储库中的镜像并管理项目
* AD/LDAP 集成：Harbor集成企业级AD/LDAP
* 审计日志：镜像存储库的全部操作均可追踪
* RESTful API：RESTful APIs 可用于管理运维，便于与外部系统集成。
* 镜像扫描: 能够自动扫描发现镜像中存在的潜在漏洞。

作为一个企业级私有Registry服务器，Harbor提供了更好的性能和安全,提升用户使用Registry构建和运行环境传输镜像的效率。Harbor支持安装在多个Registry节点的镜像资源复制，镜像全部保存在私有Registry中，确保数据和知识产权在公司内部网络中管控。另外，Harbor也提供了高级的安全特性，诸如用户管理，访问控制和活动审计等。

## 2 关于Harborclient

Harbor通过Web界面可以方便地管理用户、租户以及镜像仓库等资源，但是缺乏开发人员更喜爱的命令行管理工具，Harborclient是Harbor的第三方扩展开源工具，正弥补Harbor不足，它适合开发和运维人员管理镜像仓库、项目等资源，包含的特性如下：

* harborclient参考了OpenStack命令行工具的优秀架构和设计模式，使用也和OpenStack命令行非常类似。
* harborclient通过子命令划分不同的功能，并且所有功能是可扩展的，增加功能只需要在client下增加`do_xxx`方法即可。主模块会自动发现并注册子命令。
* 相比OpenStack的命令行工具，精简了部分复杂功能，重新设计了大多数接口，暴露的API更直观和易用。
* 支持`DEBUG`模式查看Harbor API调用过程，便于调试追踪。
* 支持`timings`选项，能够报告API请求响应时间，便于测试Harbor API性能。
* 支持https。

项目地址: `https://github.com/int32bit/harborclient`.

## 3 开始使用

### 3.1 本地安装

harborclient已经上传到pypi上，可以直接通过pip安装:

```sh
pip install python-harborclient
```

也可以直接从源码编译，harborclient使用纯Python开发，安装和部署非常简单，首先从github下拉取源代码:

```bash
git clone https://github.com/int32bit/harborclient
```

下载到本地后，进入项目主目录运行以下命令即可完成安装:

```bash
sudo pip install -r requirements.txt
sudo python setup.py install
```

安装过程中需要从互联网下载依赖包，可能需要等待几分钟。完成后运行以下命令验证是否正常运行:

```
$ harbor --os-baseurl http://localhost --os-username admin --os-project 1 info
password: ******
+------------------------------+---------------------+
| Property                     | Value               |
+------------------------------+---------------------+
| admiral_endpoint             | NA                  |
| auth_mode                    | db_auth             |
| disk_free                    | 4828315648          |
| disk_total                   | 18381979648         |
| harbor_version               | v1.2.2              |
| has_ca_root                  | False               |
| next_scan_all                | 0                   |
| project_creation_restriction | everyone            |
| registry_url                 | localhost           |
| self_registration            | True                |
| with_admiral                 | False               |
| with_clair                   | False               |
| with_notary                  | False               |
+------------------------------+---------------------+
```

以上`--os-baseurl`是Harbor的URL地址，`--os-username`是用户名，`--os-password`是密码， `--os-project`是默认的项目id，如果运行正常，将返回Harbor的信息。

每次都需要输入用户名和密码特别麻烦，harborclieng支持RC文件，从系统环境变量中读取用户信息，以`admin`用户为例，创建`~/.admin-harborrc`文件，内容如下:

```bash
export HARBOR_USERNAME=admin
export HARBOR_PASSWORD=Harbor12345
export HARBOR_URL=http://localhost
export HARBOR_PROJECT=1
```

`source`使环境变量生效：

```
source ~/.admin-harborrc
```

此时不需要再输入`--os-username`和`--os-passsword`参数，列举用户列表:

```
$ harbor user-list
+---------+----------+----------+----------------------+--------------+---------------+
| user_id | username | is_admin |        email         |   realname   |    comment    |
+---------+----------+----------+----------------------+--------------+---------------+
|    1    |  admin   |    1     |  admin@example.com   | system admin |   admin user  |
|    11   | int32bit |    0     | int32bit@example.com |   int32bit   | for int32bit  |
+---------+----------+----------+----------------------+--------------+---------------+
```

### 3.2 在Docker中运行

更建议使用Docker容器运行。harborclient托管在docker hub中，可以直接拉取已经构建的镜像到本地:

```bash
docker pull krystism/harborclient
```

docker hub中的镜像不一定是最新的，建议从源码中build镜像，在项目根下运行:

```sh
docker build -t yourname/harborclient .
```

和使用源码安装一样，需要指定harbor的用户名和密码，可以通过`docker -e`指定:

```
$ docker run \
 -e HARBOR_URL="http://localhost" \
 -e HARBOR_USERNAME="admin" \
 -e HARBOR_PASSWORD="Harbor12345" \
 -e HARBOR_PROJECT=1" \
 --rm krystism/harborclient harbor user-list
+---------+----------+----------+----------------------+--------------+---------------+
| user_id | username | is_admin |        email         |   realname   |    comment    |
+---------+----------+----------+----------------------+--------------+---------------+
|    1    |  admin   |    1     |  admin@example.com   | system admin |   admin user  |
|    11   | int32bit |    0     | int32bit@example.com |   int32bit   | for int32bit  |
+---------+----------+----------+----------------------+--------------+---------------+
```

以上命令有点长，我们可以通过设置别名简化输入:

```bash
alias harbor='docker run \
 -e HARBOR_URL="http://localhost" \
 -e HARBOR_USERNAME="admin" \
 -e HARBOR_PASSWORD="Harbor12345" \
 -e HARBOR_PROJECT=1" \
 --rm krystism/harborclient harbor'
```

此时就和使用源码安装在本地运行一样了:

```
$ harbor user-list
+---------+----------+----------+----------------------+--------------+---------------+
| user_id | username | is_admin |        email         |   realname   |    comment    |
+---------+----------+----------+----------------------+--------------+---------------+
|    1    |  admin   |    1     |  admin@example.com   | system admin |   admin user  |
|    11   | int32bit |    0     | int32bit@example.com |   int32bit   | for int32bit  |
+---------+----------+----------+----------------------+--------------+---------------+
```

## 4 命令自动补全

harborclient支持命令补全，以bash为例，需要首先安装`bash-completion`，然后执行以下命令配置自动补全：

```bash
complete -W $(harbor bash-completion) harbor
```

此时可以通过`tab`键自动补全参数以及子命令了。

```
$ harbor us<tab><tab>
usage user-create user-delete user-list user-show  user-update
```

## 5 使用https

harborclient支持https，通过`--os-cacert`选项指定CA证书，也可以通过`--insecure`跳过认证校验，相当于`curl -k`命令。

```
$ harbor list
CommandError: Unable to authorize user 'admin': Certificate verify failed, please use '--os-cacert' option to specify a CA bundle file to use in verifying a TLS (https) server certificate or use '--insecure' option to explicitly allow client to perform insecure TLS (https) requests.
$ harbor --insecure list
+-----------------------+------------+-----------+------------+------------+------------+----------------------+
|          name         | project_id |    size   | tags_count | star_count | pull_count |     update_time      |
+-----------------------+------------+-----------+------------+------------+------------+----------------------+
|    int32bit/busybox   |     2      |   715181  |     1      |     0      |     0      | 2017-11-01T07:06:36Z |
|    int32bit/golang    |     2      | 257883053 |     2      |     0      |     0      | 2017-11-01T12:59:05Z |
| int32bit/golang:1.7.3 |     2      | 257883053 |     2      |     0      |     0      | 2017-11-01T12:59:05Z |
|  int32bit/hello-world |     2      |    974    |     1      |     0      |     0      | 2017-11-01T13:22:46Z |
+-----------------------+------------+-----------+------------+------------+------------+----------------------+
```

## 5 使用文档

### 5.1 help

当运行harbor命令不指定任何参数时会打印详细的帮助信息，显示所有的子命令列表以及全局参数，如下:

```
$ harbor
usage: harbor [--debug] [--timings] [--version] [--os-username <username>]
              [--os-password <password>] [--os-project <project>]
              [--timeout <timeout>] [--os-baseurl <baseurl>] [--insecure]
              [--os-cacert <ca-certificate>] [--os-api-version <api-version>]
              <subcommand> ...

Command-line interface to the Harbor API.

Positional arguments:
  <subcommand>
    change-password             Change the password on a user that already
                                exists.
    get-cert                    Get default root cert under OVA deployment.
    get-conf                    Get system configurations.
    info                        Get general system info.
    job-list                    List filters jobs according to the policy and
                                repository.
    job-log                     Get job logs.
    ...
```

以上输出省略了部分子命令。

通过`harbor help COMMAND`可以查看详细的子命令帮助信息:

```
$ harbor help user-create
usage: harbor user-create --username <username> --password <password> --email
                          <email> [--realname <realname>]
                          [--comment <comment>]

Creates a new user account.

Optional arguments:
  --username <username>  Unique name of the new user
  --password <password>  Password of the new user
  --email <email>        Email of the new user
  --realname <realname>  Email of the new user
  --comment <comment>    Comment of the new user
```

通过帮助信息能够方便地查看各个子命令的用法。

### 5.2 debug

通过指定`--debug`参数，能够详细打印调用的harbor API以及参数，并显示response信息:

```
harbor --debug user-show 3
DEBUG (client:282) Successfully login, session id: 876a8fc6dd574c62210ed833890e6658
REQ: curl -g -i 'http://192.168.56.4/api/users/3' -X GET -H "Accept: application/json" -H "User-Agent: python-harborclient" -b "beegosessionID: 876a8fc6dd574c62210ed833890e6658"
RESP: [200] {'Date': 'Fri, 09 Sep 2016 11:20:38 GMT', 'Content-Length': '368', 'Content-Type': 'application/json; charset=utf-8', 'Connection': 'keep-alive', 'Server': 'nginx/1.9.15'}
RESP BODY: {"username": "int32bit", "comment": "", "update_time": "2016-09-07T13:05:38Z", "reset_uuid": "", "user_id": 3, "realname": "int32bit", "deleted": 0, "creation_time": "2016-09-07T13:05:38Z", "role_id": 0, "has_admin_role": 0, "role_name": "", "password": "", "Salt": "c5a5f1de-74fb-11e6-a5b4-0242ac130004", "email": "int32bit@example.com"}
```

以上我们发现调用的API为GET请求`http://192.168.56.4/api/users/3`，RESP为返回的数据，[200]表示返回的状态码为200(OK)。

### 5.3 timings

通过`--timings`参数将打印命令执行时调用的所有API列表并报告响应时间：

```
fgp@devstack:~$ harbor --timings list
+-----------------------+------------+-----------+------------+------------+------------+----------------------+
|          name         | project_id |    size   | tags_count | star_count | pull_count |     update_time      |
+-----------------------+------------+-----------+------------+------------+------------+----------------------+
|    int32bit/busybox   |     2      |   715181  |     1      |     0      |     0      | 2017-11-01T07:06:36Z |
|    int32bit/golang    |     2      | 257883053 |     2      |     0      |     0      | 2017-11-01T12:59:05Z |
| int32bit/golang:1.7.3 |     2      | 257883053 |     2      |     0      |     0      | 2017-11-01T12:59:05Z |
|  int32bit/hello-world |     2      |    974    |     1      |     0      |     0      | 2017-11-01T13:22:46Z |
+-----------------------+------------+-----------+------------+------------+------------+----------------------+
+-------------------------------------------------------------+-----------------+
| url                                                         | seconds         |
+-------------------------------------------------------------+-----------------+
| GET /repositories?project_id=2                              | 0.0804541110992 |
| GET /repositories/int32bit/busybox/tags                     | 0.0399031639099 |
| GET /repositories/int32bit/busybox/tags/latest/manifest     | 0.0498988628387 |
| GET /repositories/int32bit/golang/tags                      | 0.0701720714569 |
| GET /repositories/int32bit/golang/tags/latest/manifest      | 0.0559639930725 |
| GET /repositories/int32bit/golang/tags/1.7.3/manifest       | 0.0445079803467 |
| GET /repositories/int32bit/hello-world/tags                 | 0.04656291008   |
| GET /repositories/int32bit/hello-world/tags/latest/manifest | 0.0459671020508 |
| Total                                                       | 0.433430194855  |
+-------------------------------------------------------------+-----------------+
Total: 0.433430194855 seconds
```

从以上输出可以看出，总响应时间约为98ms。

### 5.4 timeout

通过`--timeout`参数可以设置允许的最长响应时间，单位为秒，支持浮点数，超过这个时间未响应将导致请求超时异常。

```
$ harbor --timeout 0.01 list
Traceback (most recent call last):
  File "/usr/local/bin/harbor", line 10, in <module>
    sys.exit(main())
  File "/usr/local/lib/python2.7/dist-packages/harborclient/shell.py", line 404, in main
    HarborShell().main(argv)
  File "/usr/local/lib/python2.7/dist-packages/harborclient/shell.py", line 336, in main
    args.func(self.cs, args)
    ...
    r = adapter.send(request, **kwargs)
  File "/usr/local/lib/python2.7/dist-packages/requests/adapters.py", line 521, in send
    raise ReadTimeout(e, request=request)
requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='localhost', port=443): Read timed out. (read timeout=0.01)
```

## 6 例子

### 6.1 创建用户

```
$ harbor --insecure user-create \
 --username new-user \
 --password 1q2w3e4r \
 --email new_user@example.com \
 --realname newuser \
 --comment "I am a new user"
Create user 'new-user' successfully.
```

### 6.2 删除用户

```
$ harbor --insecure user-delete new-user
Delete user 'new-user' sucessfully.
List repositories and images
```

### 6.3 查看镜像列表

```
$ harbor  list
+-----------------------+------------+-----------+------------+------------+------------+----------------------+
|          name         | project_id |    size   | tags_count | star_count | pull_count |     update_time      |
+-----------------------+------------+-----------+------------+------------+------------+----------------------+
|    int32bit/busybox   |     2      |   715181  |     1      |     0      |     0      | 2017-11-01T07:06:36Z |
| int32bit/golang:1.7.3 |     2      | 257883053 |     2      |     0      |     0      | 2017-11-01T12:59:05Z |
|  int32bit/hello-world |     2      |    974    |     1      |     0      |     0      | 2017-11-01T13:22:46Z |
+-----------------------+------------+-----------+------------+------------+------------+----------------------+
```

### 6.4 查看镜像详细信息

```
$ harbor show int32bit/golang:1.7.3
+--------------------+-------------------------------------------------------------------------+
| Property           | Value                                                                   |
+--------------------+-------------------------------------------------------------------------+
| creation_time      | 2017-11-01T12:59:05Z                                                    |
| description        |                                                                         |
| id                 | 2                                                                       |
| name               | int32bit/golang                                                         |
| project_id         | 2                                                                       |
| pull_count         | 0                                                                       |
| star_count         | 0                                                                       |
| tag_architecture   | amd64                                                                   |
| tag_author         |                                                                         |
| tag_created        | 2016-11-08T19:32:39.908048617Z                                          |
| tag_digest         | sha256:37d263ccd240e113a752c46306ad004e36532ce118eb3131d9f76f43cc606d5d |
| tag_docker_version | 1.12.3                                                                  |
| tag_name           | 1.7.3                                                                   |
| tag_os             | linux                                                                   |
| tag_signature      | -                                                                       |
| tags_count         | 2                                                                       |
| update_time        | 2017-11-01T12:59:05Z                                                    |
+--------------------+-------------------------------------------------------------------------+
```

### 6.5 查看最热门镜像

```
$ harbor top
+----------------------+------------+------------+
|         name         | pull_count | star_count |
+----------------------+------------+------------+
|   int32bit/busybox   |     10     |     0      |
|   int32bit/golang    |     8      |     0      |
| int32bit/hello-world |     1      |     0      |
+----------------------+------------+------------+
```

### 6.6 查看用户角色

```
$ harbor member-list
+----------+--------------+---------+---------+
| username |  role_name   | user_id | role_id |
+----------+--------------+---------+---------+
|  admin   | projectAdmin |    1    |    1    |
|   foo    |  developer   |    5    |    2    |
|   test   |    guest     |    6    |    3    |
+----------+--------------+---------+---------+
```

### 6.7 查看日志

```
$ harbor logs
+--------+----------------------+----------+------------+-----------+-----------------------------+
| log_id |       op_time        | username | project_id | operation |          repository         |
+--------+----------------------+----------+------------+-----------+-----------------------------+
|   1    | 2017-11-01T06:56:07Z |  admin   |     2      |   create  |          int32bit/          |
|   2    | 2017-11-01T07:06:36Z |  admin   |     2      |    push   |   int32bit/busybox:latest   |
|   3    | 2017-11-01T12:59:05Z |  admin   |     2      |    push   |    int32bit/golang:1.7.3    |
|   4    | 2017-11-01T13:22:46Z |  admin   |     2      |    push   | int32bit/hello-world:latest |
|   5    | 2017-11-01T14:21:49Z |  admin   |     2      |    push   |    int32bit/golang:latest   |
|   6    | 2017-11-03T20:39:04Z |  admin   |     3      |   create  |            test/            |
|   7    | 2017-11-03T20:39:22Z |  admin   |     3      |   delete  |            test/            |
|   8    | 2017-11-03T20:39:38Z |  admin   |     4      |   create  |            test/            |
|   9    | 2017-11-03T20:49:33Z |  admin   |     4      |   delete  |            test/            |
+--------+----------------------+----------+------------+-----------+-----------------------------+
```

### 6.8 搜索

```
$ harbor search int32bit
Find 1 Projects:
+------------+----------+--------+------------+----------------------+
| project_id |   name   | public | repo_count |    creation_time     |
+------------+----------+--------+------------+----------------------+
|     2      | int32bit |   1    |     3      | 2017-11-01T06:56:07Z |
+------------+----------+--------+------------+----------------------+

Find 3 Repositories:
+----------------------+--------------+------------+----------------+
|   repository_name    | project_name | project_id | project_public |
+----------------------+--------------+------------+----------------+
|   int32bit/busybox   |   int32bit   |     2      |       1        |
|   int32bit/golang    |   int32bit   |     2      |       1        |
| int32bit/hello-world |   int32bit   |     2      |       1        |
+----------------------+--------------+------------+----------------+
```

### 6.9 查看复制目标

```
$ harbor target-list
+----+----------------------+-------------------------------------+----------+----------+----------------------+
| id |         name         |               endpoint              | username | password |    creation_time     |
+----+----------------------+-------------------------------------+----------+----------+----------------------+
| 1  |     test-target      |      http://192.168.99.101:8888     |  admin   |    -     | 2017-11-02T01:35:30Z |
| 2  |    test-target-2     |      http://192.168.99.101:9999     |  admin   |    -     | 2017-11-02T13:43:07Z |
| 3  | int32bit-test-target | http://192.168.99.101:8888/int32bit |  admin   |    -     | 2017-11-02T14:28:54Z |
+----+----------------------+-------------------------------------+----------+----------+----------------------+
```

### 6.10 ping复制目标镜像仓库

```
$ harbor target-ping 1
OK
```

### 6.11 查看复制任务

```
$ harbor  job-list 1
+----+----------------------+-----------+----------+----------------------+
| id |      repository      | operation |  status  |     update_time      |
+----+----------------------+-----------+----------+----------------------+
| 1  |   int32bit/busybox   |  transfer | finished | 2017-11-02T01:35:31Z |
| 2  |   int32bit/golang    |  transfer | finished | 2017-11-02T01:35:31Z |
| 3  | int32bit/hello-world |  transfer | finished | 2017-11-02T01:35:31Z |
+----+----------------------+-----------+----------+----------------------+
```

### 6.12 查看复制任务日志

```
$ harbor job-log  1
2017-11-02T01:35:30Z [INFO] initializing: repository: int32bit/busybox, tags: [], source URL: http://registry:5000, destination URL: http://192.168.99.101:8888, insecure: false, destination user: admin
2017-11-02T01:35:30Z [INFO] initialization completed: project: int32bit, repository: int32bit/busybox, tags: [latest], source URL: http://registry:5000, destination URL: http://192.168.99.101:8888, insecure: false, destination user: admin
2017-11-02T01:35:30Z [WARNING] the status code is 409 when creating project int32bit on http://192.168.99.101:8888 with user admin, try to do next step
2017-11-02T01:35:30Z [INFO] manifest of int32bit/busybox:latest pulled successfully from http://registry:5000: sha256:030fcb92e1487b18c974784dcc110a93147c9fc402188370fbfd17efabffc6af
2017-11-02T01:35:30Z [INFO] all blobs of int32bit/busybox:latest from http://registry:5000: [sha256:54511612f1c4d97e93430fc3d5dc2f05dfbe8fb7e6259b7351deeca95eaf2971 sha256:03b1be98f3f9b05cb57782a3a71a44aaf6ec695de5f4f8e6c1058cd42f04953e]
2017-11-02T01:35:31Z [INFO] blob sha256:54511612f1c4d97e93430fc3d5dc2f05dfbe8fb7e6259b7351deeca95eaf2971 of int32bit/busybox:latest already exists in http://192.168.99.101:8888
2017-11-02T01:35:31Z [INFO] blob sha256:03b1be98f3f9b05cb57782a3a71a44aaf6ec695de5f4f8e6c1058cd42f04953e of int32bit/busybox:latest already exists in http://192.168.99.101:8888
2017-11-02T01:35:31Z [INFO] blobs of int32bit/busybox:latest need to be transferred to http://192.168.99.101:8888: []
2017-11-02T01:35:31Z [INFO] manifest of int32bit/busybox:latest exists on source registry http://registry:5000, continue manifest pushing
2017-11-02T01:35:31Z [INFO] manifest of int32bit/busybox:latest exists on destination registry http://192.168.99.101:8888, skip manifest pushing
2017-11-02T01:35:31Z [INFO] no tag needs to be replicated, next state is "finished"
```

### 6.13 查看资源统计

```
$ harbor usage
+-----------------------+-------+
| Property              | Value |
+-----------------------+-------+
| private_project_count | 0     |
| private_repo_count    | 0     |
| public_project_count  | 2     |
| public_repo_count     | 3     |
| total_project_count   | 2     |
| total_repo_count      | 3     |
+-----------------------+-------+
```

### 6.14 查看harbor信息

```
$ harbor  info
+------------------------------+---------------------+
| Property                     | Value               |
+------------------------------+---------------------+
| admiral_endpoint             | NA                  |
| auth_mode                    | db_auth             |
| disk_free                    | 4989370368          |
| disk_total                   | 18381979648         |
| harbor_version               | v1.2.2              |
| has_ca_root                  | False               |
| next_scan_all                | 0                   |
| project_creation_restriction | everyone            |
| registry_url                 | 192.168.99.101:8888 |
| self_registration            | True                |
| with_admiral                 | False               |
| with_clair                   | False               |
| with_notary                  | False               |
+------------------------------+---------------------+
```

### 6.15 查看harbor配置信息

```
$ harbor get-conf
+------------------------------+-------------------------------------------------------+----------+
|             name             |                         value                         | editable |
+------------------------------+-------------------------------------------------------+----------+
|          auth_mode           |                        db_auth                        |  False   |
|          email_from          |           admin <sample_admin@mydomain.com>           |   True   |
|          email_host          |                   smtp.mydomain.com                   |   True   |
|        email_identity        |                           -                           |   True   |
|          email_port          |                           25                          |   True   |
|          email_ssl           |                         False                         |   True   |
|        email_username        |               sample_admin@mydomain.com               |   True   |
|         ldap_base_dn         |              ou=people,dc=mydomain,dc=com             |   True   |
|         ldap_filter          |                           -                           |   True   |
|          ldap_scope          |                           3                           |   True   |
|        ldap_search_dn        |                           -                           |   True   |
|         ldap_timeout         |                           5                           |   True   |
|           ldap_uid           |                          uid                          |   True   |
|           ldap_url           |               ldaps://ldap.mydomain.com               |   True   |
| project_creation_restriction |                        everyone                       |   True   |
|       scan_all_policy        | {u'parameter': {u'daily_time': 0}, u'type': u'daily'} |   True   |
|      self_registration       |                          True                         |   True   |
|       token_expiration       |                           30                          |   True   |
|      verify_remote_cert      |                          True                         |   True   |
+------------------------------+-------------------------------------------------------+----------+
```

### 6.16 修改用户密码

```
$ harbor change-password int32bit
Old password: *****
New Password: *****
Retype new Password: *****
Update password successfully.
```


### 6.17 设置用户为管理员

```
$ harbor promote int32bit
Promote user 'int32bit' as administrator successfully.
```

## 7 如何增加一个子命令?

以增加一个`echo`子命令为例，首先在`harborclient/v2`目录下新创建一个模块文件`tests.py`，实现`echo`方法，如下:

```python
from harborclient import base
class TestManager(base.Manager):
    def echo(self, message):
        return message
```

在`harborclient/v2/client`中注册`TestManager`：

```python
... # 省略其它import
from harborclient.v2 import tests
class Client(object):
    def __init__(self,
                 username=None,
                 password=None,
                 project=None,
                 baseurl=None,
                 insecure=False,
                 cacert=None,
                 api_version=None,
                 *argv,
                 **kwargs):
        ... # 省略其它Manager
        self.tests = tests.TestManager(self)
```

最后在`harborclient/v2/shell.py`中注册新的子命令，注意在`shell.py`中所有的`do_xx`方法都会对应一条子命令，转化规则为:

```
do_a_b_c => a-b-c
比如:
do_user_list => user-list
do_project_show => project-show
```

方法的`doc文档`将转化为`echo`子命令的帮助信息。

因此新增`echo`子命令，只需要在`shell.py`中新增`do_echo`方法：

```python
@utils.arg(
    '--message',
    metavar='<message>',
    dest='message',
    required=True,
    help='The message to print.')
def do_echo(cs, args):
    """Print a message."""
    message = cs.tests.echo(args.message)
    print(message)
```

此时`echo`子命令就实现了。

查看帮助信息:

```
$ harbor  help echo
usage: harbor echo --message <message>

Print a message.

Optional arguments:
  --message <message>  The message to print.
```

执行子命令:

```
$ harbor  echo --message 'HelloWorld!'
HelloWorld!
```

## 8 协议

[Apache License 2.0](./LICENSE)
