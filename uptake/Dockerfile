# Last ubuntu version
FROM ubuntu:22.04

# Sets MongoDB version
ENV MONGO_VERSION 7.0
ENV UBUNTU_CODE_NAME jammy
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install both Python 3 and MongoDB latest
RUN apt-get update && \
    apt-get install -y wget gnupg tzdata && \
    uname -m && \
    wget -qO - https://www.mongodb.org/static/pgp/server-${MONGO_VERSION}.asc | \
    gpg -o /usr/share/keyrings/mongodb-server-${MONGO_VERSION}.gpg --dearmor && \
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-${MONGO_VERSION}.gpg ] https://repo.mongodb.org/apt/ubuntu ${UBUNTU_CODE_NAME}/mongodb-org/${MONGO_VERSION} multiverse" | tee /etc/apt/sources.list.d/mongodb-org-${MONGO_VERSION}.list && \
    apt-get update && \
    apt-get install -y mongodb-org python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Copy Python3 requirements
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip3 install -r /app/requirements.txt

# Copy Python script to app folder
COPY app/generate_uptakes.py /app/generate_uptakes.py

# Expose MongoDB port
EXPOSE 27017

# Create MongoDB data folder
RUN mkdir -p /data/db
RUN mkdir -p /data/dump

# Launch services
CMD ["sh", "-c", "mongod --bind_ip_all & sleep 5 && tail -f /dev/null"]