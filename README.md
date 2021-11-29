### 配置部署

#### 一、安装依赖库

利用 **`pip`** 安装依赖文件，执行下面命令：

```shell
$ pip install -r requirements.txt 
```

#### 二、配置环境变量

重点配置 `DJANGO_DEBUG` 和 `DJANGO_SECRET_KEY`。

可以在本地创建一个新的文件 `.env` 并且在文件里面配置这两个字段，示例参考：

```shell
# 配置 SECRET_KEY 主要用于 csrf 等需要加密的key
export DJANGO_SECRET_KEY='<your_secret_key>'
# 关闭DEBUG模式
export DJANGO_DEBUG=False
```

在你的`bash`环境里面生效该配置：

```shell
$ source .env
```

##### 补充：如何配置 Secret Key

访问链接 👉 [Django Secret Key Generator](https://miniwebtool.com/django-secret-key-generator/)

生成类似如下内容：

```shell
Generated Django Secret Key: `)rsa&jco3oesj537#$la$f6*j0or!!eimi&=#5%+a!!$(o265&`
```

复制冒号的内容填到替换 `<your_secret_key>`

⚠️注意：默认的Django `django-admin startproject` 会自动创建`SECRET_KEY`  为每一个新建的项目。格式类似如下：

```shell
DJANGO_SECRET_KEY='django-insecure-kur#75*^bdh)um8=n=rq5nj7^(ew8is=g&z8duyc2bzew^y5gc'
```

#### 三、初始化项目

##### 3.1 初始化配置

执行数据库初始化

```shell
$./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, records, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying records.0001_initial... OK
  Applying records.0002_auto_20211016_0700... OK
  Applying records.0003_auto_20211021_1527... OK
  Applying records.0004_alter_report_created_at... OK
  Applying sessions.0001_initial... OK
```

执行之后我们数据库就初始化完毕了。

##### 3.2 创建管理员账号

```shell
$./manage.py createsuperuser
用户名 (leave blank to use 'javan'): master
电子邮件地址: javanyouchn@gmail.com
Password:
Password (again):
Superuser created successfully.
```

按着步骤输入自己的选择即可。

##### 3.3 启动服务

在`bash` 环境输入：

```shell
$ ./manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
November 29, 2021 - 15:01:53
Django version 3.2.8, using settings 'codermind.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

#### 四、使用介绍

##### 4.1 访问后台

在浏览器输入 `http://127.0.0.1:8000/admin`, 使用已创建管理员账号登录信息

**创建账户**：

在 **认证和授权** 分组下的**用户**分组里面点击 ***增加*** 为自己的团队成员创建账号；

**周报计划表**：——团队具体周报填写周期安排

每个周报计划条目需要填写三个具体信息：

1. 开始日期——周报的起始时间点
2. 结束日期——周报统计的结束时间点
3. 公休天数——周期内法定休息时间；

[2021-11-24, 2021-11-30] 是一个双向闭区间

**项目列表**：

提交配置团队可以填写的具体项目选项。方便通过项目进行人力的分配计算。

##### 4.2 使用系统

在浏览器输入 `http://127.0.0.1:8000/records`

