FROM centos:6.6

RUN yum install -y \
    curl \
    gcc \
    git \
    httpd \
    httpd-devel \
    libaio \
    nc.x86_64 \
    openssl \
    openssl-devel \
    tar \
    unzip \
    zlib-devel \
    mysql-devel

RUN mkdir /rfam-api
RUN mkdir /rfam-api/local

ENV LOC /rfam-api/local

# Install Python
RUN \
    cd $LOC && \
    curl -OL http://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz && \
    tar -zxvf Python-3.6.2.tgz && \
    cd Python-3.6.2 && \
    PREFIX=$LOC/python-3.6.2/ && \
    export LD_RUN_PATH=$PREFIX/lib && \
    ./configure --prefix=$PREFIX  --enable-shared && \
    make && \
    make install && \
    cd $LOC && \
    rm -Rf Python-3.6.2 && \
    rm Python-3.6.2.tgz

# Install virtualenv
RUN \
    cd $LOC && \
    curl -OL  https://pypi.python.org/packages/source/v/virtualenv/virtualenv-15.0.1.tar.gz && \
    tar -zxvf virtualenv-15.0.1.tar.gz && \
    cd virtualenv-15.0.1 && \
    $LOC/python-3.6.2/bin/python3 setup.py install && \
    cd $LOC && \
    rm -Rf virtualenv-15.0.1.tar.gz && \
    rm -Rf virtualenv-15.0.1

# Create virtual environment
RUN \
    cd $LOC && \
    mkdir virtualenvs && \
    cd virtualenvs && \
    $LOC/python-3.6.2/bin/virtualenv rfam-api --python=$LOC/python-3.6.2/bin/python3

# Define container environment variables
ENV RFAM_API_HOME /rfam-api/rfam-api

# Install Django requirements
ADD api/requirements.txt $RFAM_API_HOME/api/
RUN \
    source $LOC/virtualenvs/rfam-api/bin/activate && \
    pip install -r $RFAM_API_HOME/api/requirements.txt

# Expose a container port where the website is served
EXPOSE 4000

# Start up the app
ENTRYPOINT \
    source $LOC/virtualenvs/rfam-api/bin/activate && \
    echo 'The server is running at localhost:4000' && \
    python $RFAM_API_HOME/api/manage.py runserver 0.0.0.0:4000
