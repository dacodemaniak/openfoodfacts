FROM openjdk:8-jdk-slim

# Python installation
RUN apt-get update && apt-get install -y python3 python3-pip wget

# PySpark and dependencies
RUN pip3 install pyspark pymongo

# Connectors installation _2.12:10.4.0
RUN wget https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/10.4.0/mongo-spark-connector_2.12-10.4.0.jar -P /opt/spark/jars/

# Download and install Apache Spark
RUN wget https://downloads.apache.org/spark/spark-3.5.2/spark-3.5.2-bin-hadoop3.tgz
RUN tar -xvzf spark-3.5.2-bin-hadoop3.tgz
RUN mkdir -p /opt/spark
RUN cp -R spark-3.5.2-bin-hadoop3/* /opt/spark
RUN rm -rf spark-3.5.2-bin-hadoop3
RUN rm spark-3.5.2-bin-hadoop3.tgz

# Sets environment vars
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Copy py script
COPY app/extract_and_merge.py /opt/spark-apps/extract_and_merge.py

CMD ["/opt/spark/bin/spark-submit", "--packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0", "/opt/spark-apps/extract_and_merge.py"]