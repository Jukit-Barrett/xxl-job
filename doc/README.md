

# install

````shell
java -jar $JAVA_OPTS ./xxl-job-admin-3.2.1-SNAPSHOT.jar $PARAMS

java -jar $JAVA_OPTS ./xxl-job-executor-sample-springboot-3.2.1-SNAPSHOT.jar $PARAMS

mvn install:install-file \
  -Dfile=/Users/jukit/opt/disk/java/xxl-job/xxl-job-core/target/xxl-job-core-3.2.1-SNAPSHOT.jar \
  -DgroupId=com.xuxueli \
  -DartifactId=xxl-job-core \
  -Dversion=3.2.1-SNAPSHOT \
  -Dpackaging=jar
````

# MySQL
MYSQL_HOST=115.190.154.216
MYSQL_PORT=3306
MYSQL_DATABASE=xxl_job
MYSQL_USERNAME=root
MYSQL_PASSWORD="W_oypi6PsNK@NY;F<}!!6z[{8Bk"
MYSQL_PREFIX=sf_