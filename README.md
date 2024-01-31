# oo运维系统后端

框架：Django 3.2

语言：Python 3.10

## Prepare

安装mysql-server，并创建一个新的database：

```sql
create database oosys

create user 'ooroot'@'%' identified by '123456';
grant all privileges on *.* to 'ooroot'@'%';
flush privileges;
```

将oosys_backup.sql导入

```sql
mysql -u ooroot -p oosys

source oosys_backup.sql
```

然后在settings.py指定数据库：

```py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "oosys",
        "USER": "ooroot",
        "PASSWORD": "123456",
        "HOST": "10.0.0.211",
        "PORT": "3306",
    }
}
```



## Usage

### Dockerfile

```dockerfile
FROM python:3.10

ADD . /app

WORKDIR /app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

RUN pip install --no-cache-dir -r requirements

RUN apt-get update && apt-get install -y \
        libc6-dev \
        gcc \
        mime-support \
    && pip install --no-cache-dir uWSGI \
    && apt-get remove -y \
        gcc \
        libc6-dev \
    && rm -rf /var/lib/apt/lists/*

CMD ["uwsgi", "--wsgi-file", "oo/wsgi.py", "--http", ":8000", "--stats", ":8001", "--stats-http"]

EXPOSE 8000 8001
```

创建镜像：

```sh
docker build -t oo-django .
```

运行

```sh
docker run -d -p 8000:8000 -p 8001:8001 oo-django
```

