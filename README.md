
# XXL JOB 安装

````shell
docker build --progress=plain -f dockerfile -t openjdk:21-jdk-slim-v1 .
````


- 启动
````shell
java -jar $JAVA_OPTS ./xxl-job-executor-sample-springboot-3.2.1-SNAPSHOT.jar $PARAMS
````

# 备份（不用执行）

````shell
mvn install:install-file \
  -Dfile=/Users/jukit/opt/disk/java/xxl-job/xxl-job-core/target/xxl-job-core-3.2.1-SNAPSHOT.jar \
  -DgroupId=com.xuxueli \
  -DartifactId=xxl-job-core \
  -Dversion=3.2.1-SNAPSHOT \
  -Dpackaging=jar
````
