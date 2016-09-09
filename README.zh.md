## 1 什么是Harbor？

Harbor是由VMware中国研发团队负责开发的开源企业级Registry项目，项目地址为`https://github.com/vmware/harbor`，该项目发布5个多月以来，深受用户喜爱，在GitHub获得了1000多个点赞星星和200多个Forks。

它是一个用于存储和分发Docker镜像的企业级Registry服务器，通过添加一些企业必需的功能特性，例如安全、标识和管理等，扩展了开源Docker Distribution，提供了:

* 基于角色的访问控制：用户和存储库是通过“项目”关联，同时用户对同一“项目”下镜像拥有不同访问权限。
* 镜像远程复制（同步）：镜像可以在多个注册表之间复制（同步）。支持负载均衡，高可用性，混合云及多种云的情况。
* 图形管理界面：用户能够快捷浏览、搜索存储库中的镜像并管理项目
* AD/LDAP 集成：Harbor集成企业级AD/LDAP
* 审计日志：镜像存储库的全部操作均可追踪
* RESTful API：RESTful APIs 可用于管理运维，便于与外部系统集成。

作为一个企业级私有Registry服务器，Harbor提供了更好的性能和安全,提升用户使用Registry构建和运行环境传输镜像的效率。Harbor支持安装在多个Registry节点的镜像资源复制，镜像全部保存在私有Registry中，确保数据和知识产权在公司内部网络中管控。另外，Harbor也提供了高级的安全特性，诸如用户管理，访问控制和活动审计等。

## 2 关于Harborclient

Harbor通过Web界面可以方便地管理用户、租户以及镜像仓库，但是缺乏开发人员更喜爱的命令行管理工具，Harborclient是Harbor的第三方扩展开源工具，正弥补Harbor不足，它更适合开发和运维人员管理镜像仓库，其特性包括：

* Harborclient参考了Openstack命令行工具的架构和设计模式，使用也和Openstack命令行非常类似。
* Harborclient通过子命令划分不同的功能，并且所有功能是可扩展的，增加功能只需要在client下增加`do_xxx`方法即可。主模块会自动发现功能模块。
* 相比Openstack的命令行工具，精简了复杂部分，重新设计了大多数接口，暴露的API更直观和易用。
* 支持`DEBUG`模式查看Harbor API调用过程，便于调试追踪。
* 支持`timings`，能够报告API请求响应时间，便于测试Harbor API性能。

项目地址: `https://github.com/int32bit/harborclient`

接下来本文将详细介绍Harborclient的使用。

## 3 开始使用

### 3.1 源码安装

Harborclieng使用Python开发，非常容易的安装部署，首先从github下拉取源代码:

```bash
git clone https://github.com/int32bit/harborclient
```

下载到本地后，进入项目运行以下命令即可完成安装:

```bash
sudo pip install -r requirements.txt
sudo python setup.py install
```
安装过程中需要从互联网下载依赖包，需要耐心等待几分钟。完成后运行以下命令验证是否正常运行:

```
$ harbor --os-baseurl http://localhost login --username admin --password Harbor12345
Successfully login, session id: 989a01ccd500a44f9908939dc96822b3
```
以上`--os-baseurl`是Harbor的URL地址，`--username`是用户名，`--password`是用户密码，如果运行正常，将返回登录成功信息并返回`session id`。

每次都需要输入用户名和密码特别麻烦，Harborclieng支持RC文件，从系统环境变量中读取用户信息，以`admin`用户为例，创建`~/.admin-harborrc`文件，写入以下内容:

```
export HARBOR_USERNAME=admin
export HARBOR_PASSWORD=Harbor12345
export HARBOR_URL=http://localhost
export HARBOR_PROJECT=1
```

`source`使变量生效：

```
source ~/.admin-harborrc
```

不需要再输入`--username`和`--passsword`参数，列举用户列表:

```
$ harbor user-list
+---------+----------+----------------------+--------------+-------------+
| user_id | username |        email         |   realname   |   comment   |
+---------+----------+----------------------+--------------+-------------+
|    3    | int32bit | int32bit@example.com |   int32bit   |      -      |
|    4    |  harbor  |  harbor@example.com  | harbor@12345 | harbor test |
+---------+----------+----------------------+--------------+-------------+
```

### 3.2 使用Docker容器运行

从源码安装需要一系列的配置，并且Mac平台下还有点问题，因此本文更建议使用Docker容器运行。使用步骤如下。

#### 3.2.1 获取Harborclient镜像

Harborclient已经托管在Dockerhub，因此能够直接拉取镜像到本地:

```bash
docker pull krystism/harborclient
```

同时也支持自己构建镜像，在项目根下运行即可:

```
docker build -t yourname/harborclient .
```

#### 3.2.2 运行HarborClient容器

和使用源码安装一样，需要指定用户名和密码，可以通过`docker -e`指定:

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

以上`--net`指定网络模式，这并不是必需的，只要能够保证容器能够访问Harbor API即可。

以上命令略显复杂，可以通过设置别名简化输入:

```bash
alias harbor='docker run \
 -e HARBOR_USERNAME="admin" \
 -e HARBOR_PASSWORD="Harbor12345" \
 -e HARBOR_URL="http://192.168.56.4" \
 --net host --rm krystism/harborclient'
```

此时就和使用源码安装在本地运行一样了:

```
$ harbor user-list
+---------+----------+----------------------+--------------+-------------+
| user_id | username |        email         |   realname   |   comment   |
+---------+----------+----------------------+--------------+-------------+
|    3    | int32bit | int32bit@example.com |   int32bit   |      -      |
|    4    |  harbor  |  harbor@example.com  | harbor@12345 | harbor test |
+---------+----------+----------------------+--------------+-------------+
```

## 4 用户使用文档

接下来将详细介绍如何使用HarborClient以及功能介绍，HarborClient支持非常详细的帮助信息，用户可以随时使用`help`命令查看具体帮助信息，因此本文不会介绍所有的用法和参数。

### 4.1 通用技巧

HarborClient支持一些和子命令无关的全局参数，实现特定附加的功能。

#### 4.1.1 善用帮助

当运行harbor命令不指定任何参数时会打印详细的帮助信息，显示所有的子命令列表以及全局参数，如下:

```
usage: harbor [--debug] [--timings] [--version] [--os-username <username>]
              [--os-password <password>] [--timeout <timeout>]
              [--os-baseurl <baseurl>] [--os-api-version <api-version>]
              <subcommand> ...

Command-line interface to the Harbor API.

Positional arguments:
  <subcommand>
    list                        Print a list of available 'repositories'.
	... 
    bash-completion             Prints all of the commands and options to
                                stdout so that the harbor.bash_completion
                                script doesn't have to hard code them.
    help                        Display help about this program or one of its
                                subcommands.

Optional arguments:
  --debug                       Print debugging output.
  --timings                     Print call timing info.
  --version                     show program's version number and exit
  --os-username <username>      Username
  --os-password <password>      User's password
  --timeout <timeout>           Set request timeout (in seconds).
  --os-baseurl <baseurl>        API base url
  --os-api-version <api-version>
                                Accepts X, X.Y (where X is major and Y is
                                minor part) or "X.latest", defaults to
                                env[HARBOR_API_VERSION].

See "harbor help COMMAND" for help on a specific command.
```
以上输出省略了部分子命令。

通过`harbor help COMMAND`可以查看详细的子命令帮助信息:

```
usage: harbor user-create --username <username> --password <password> --email
                          <email> [--realname <realname>]
                          [--comment <comment>]

Create a new User.

Optional arguments:
  --username <username>  Unique name of the new user.
  --password <password>  Password of the new user.
  --email <email>        Email of the new user.
  --realname <realname>  Realname of the new user.
  --comment <comment>    Comment of the new user.
```

通过帮助信息能够方便地查看各个子命令的用法。

#### 4.1.2 开启DEBUG模式

通过指定`--debug`参数，能够详细打印调用的API地址以及参数，并显示Response信息:

```
harbor --debug user-show 3
DEBUG (client:282) Successfully login, session id: 876a8fc6dd574c62210ed833890e6658
REQ: curl -g -i 'http://192.168.56.4/api/users/3' -X GET -H "Accept: application/json" -H "User-Agent: python-harborclient" -b "beegosessionID: 876a8fc6dd574c62210ed833890e6658"
RESP: [200] {'Date': 'Fri, 09 Sep 2016 11:20:38 GMT', 'Content-Length': '368', 'Content-Type': 'application/json; charset=utf-8', 'Connection': 'keep-alive', 'Server': 'nginx/1.9.15'}
RESP BODY: {"username": "int32bit", "comment": "", "update_time": "2016-09-07T13:05:38Z", "reset_uuid": "", "user_id": 3, "realname": "int32bit", "deleted": 0, "creation_time": "2016-09-07T13:05:38Z", "role_id": 0, "has_admin_role": 0, "role_name": "", "password": "", "Salt": "c5a5f1de-74fb-11e6-a5b4-0242ac130004", "email": "int32bit@example.com"}
```

以上我们发现调用的API为GET请求`http://192.168.56.4/api/users/3`，返回的数据是User model的json数据。

#### 4.1.3 统计API响应时间

通过`--timings`参数将打印命令执行时调用的所有API列表并报告响应时间：

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

从以上输出可以看出，总响应时间约为98ms。

#### 4.1.4 设置响应超时

通过`--timeout`参数可以设置允许的最长响应时间，单位为秒，超过这个时间将导致请求超时异常。

```bash
harbor --timeout 1 list
```

以上设置允许总的时间不超过1秒。

### 4.2 用户管理

#### 4.2.1 列举用户列表

使用`user-list`子命令可以查看系统的用户列表，指定`--sortby`参数可以设置排序的key。

#### 4.2.2 查看用户详细信息

使用`user-show`子命令查看用户的详细信息，其用法为:

```
harbor user-show <user>
```

其中`<user>`参数可以是用户id或者用户名。

```
harbor user-show int32bit
+----------------+--------------------------------------+
| Property       | Value                                |
+----------------+--------------------------------------+
| Salt           | c5a5f1de-74fb-11e6-a5b4-0242ac130004 |
| comment        |                                      |
| creation_time  | 2016-09-07T13:05:38Z                 |
| deleted        | 0                                    |
| email          | int32bit@example.com                 |
| has_admin_role | 0                                    |
| password       |                                      |
| realname       | int32bit                             |
| reset_uuid     |                                      |
| role_id        | 0                                    |
| role_name      |                                      |
| update_time    | 2016-09-07T13:05:38Z                 |
| user_id        | 3                                    |
| username       | int32bit                             |
+----------------+--------------------------------------+
```

**注意**：该命令支持指定用户名查找用户，但`admin`用户除外，因为`admin`用户在list列表中不存在，但可以通过指定admin的ID查看admin用户的详细信息，admin的ID通常为1。

#### 4.2.3 创建用户

```
usage: harbor user-create --username <username> --password <password> --email
                          <email> [--realname <realname>]
                          [--comment <comment>]
```
创建用户必须指定`--username`、`--password`以及`--email`参数，其它可以留空。

```
$ harbor user-create --username test_harbor \
--password Harbor12345 \
--email harbor_test@example.com \
--comment "Just for testing"
Create user 'test_harbor' successfully.
```

#### 4.2.4 删除用户

通过`user-delete`删除用户，必须指定用户ID或者用户名:

```
$ harbor user-delete test_harbor
Delete user 'test_harbor' sucessfully.
```

#### 4.2.5 更新用户信息

使用`user-update`子命令可以更新用户信息。

#### 4.2.6 修改用户密码

使用`user-change-password`子命令修改用户密码。

### 4.3 租户管理

租户(Project)管理和用户管理基本类似，本文不再详细介绍，细节可查看帮助信息。

### 4.4 镜像管理

#### 4.4.1 查看镜像列表

查看镜像列表是最常用的操作，直接使用`list`子命令即可查看所有的镜像列表，包括名称和tags等.

```
$ harbor --timings list
+--------------+----------------+-------+---------+--------------+-------+
|      Id      |      Name      |  Tag  | Project | Architecture |   OS  |
+--------------+----------------+-------+---------+--------------+-------+
| 06cc1800c7a4 | library/ubuntu | 14.04 |    1    |    amd64     | linux |
+--------------+----------------+-------+--------+---------+-------------+
```

注意Id截取了前12位。

#### 4.4.2 查看镜像详细信息

使用`show`子命令查看镜像的详细信息:

```
$ harbor show ubuntu:14.04
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

#### 4.4.3 查看镜像的tag列表

通过`list-tags`显示镜像的所有的标签列表:

```
harbor list-tags library/ubuntu
+-------+
|  Tag  |
+-------+
| 14.04 |
| 12.04 |
+-------+
```

### 4.5 查看日志

HarborClient支持查看操作日志功能，使用`logs`子命令查看:

```
$ harbor logs
+----------------------+----------+-----------+----------------------+
|       op_time        | username | operation |      repository      |
+----------------------+----------+-----------+----------------------+
| 2016-09-07T13:08:41Z |  admin   |    push   | library/ubuntu:14.04 |
| 2016-09-07T13:25:41Z |  admin   |   create  |      int32bit/       |
| 2016-09-07T13:25:55Z |  admin   |   create  |      krystism/       |
| 2016-09-07T21:40:08Z |  admin   |    pull   | library/ubuntu:14.04 |
| 2016-09-07T21:40:11Z |  admin   |    pull   | library/ubuntu:14.04 |
+----------------------+----------+-----------+----------------------+
```

### 4.6 查看租户统计信息

```
harbor stat
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

### 4.7 查看热门镜像

```
harbor top
+----------------+-------+
|      name      | count |
+----------------+-------+
| library/ubuntu |   8   |
| library/python |   5   |
| library/centos |   2   |
+----------------+-------+
```

### 4.8 搜索

通过`search`子命令并指定关键字query，搜索匹配的租户列表和镜像列表:

```
$ harbor search ubuntu
Find 0 Projects:
+----+------+--------+
| id | name | public |
+----+------+--------+
+----+------+--------+

Find 1 Repositories:
+-----------------+--------------+------------+----------------+
| repository_name | project_name | project_id | project_public |
+-----------------+--------------+------------+----------------+
|  library/ubuntu |   library    |     1      |       1        |
+-----------------+--------------+------------+----------------+
```

## 5 已知问题

1. project不支持删除操作。
2. `user-show`不能指定`admin`用户名。
3. 删除用户后再创建相同用户名时会失败。
