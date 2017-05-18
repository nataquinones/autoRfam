#
# Dockerfile to create a reproducible installation of the autoRfam pipeline
# 
#
# About the mounted volume:
#   /autorfam/autorfam-code is a mounted volume defined in
#    docker-compose.yml as ${AUTORFAM_VOL}:/autorfam/autorfam-code
#    or in
#    docker run -v ${AUTORFAM_VOL}:/autorfam/autorfam-code
#    where AUTORFAM_VOL=/path/to/autorfam/code
#


FROM centos:6.6

RUN yum install -y \
    curl \
    gcc-c++ \
    git \
    gnuplot \
    libaio \
    openssl \
    openssl-devel \
    tar \
    unzip \
    zlib-devel

RUN mkdir /autorfam
RUN mkdir /autorfam/local

ENV RUT /autorfam
ENV LOC /autorfam/local
ENV MOUNT /autorfam/autorfam-code

# Install Python
RUN \
    cd $LOC && \
    curl -OL http://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz && \
    tar -zxvf Python-2.7.11.tgz && \
    cd Python-2.7.11 && \
    PREFIX=$LOC/python-2.7.11/ && \
    export LD_RUN_PATH=$PREFIX/lib && \
    ./configure --prefix=$PREFIX  --enable-shared && \
    make && \
    make install && \
    cd $LOC && \
    rm -Rf Python-2.7.11 && \
    rm Python-2.7.11.tgz

# Install virtualenv
RUN \
    cd $LOC && \
    curl -OL  https://pypi.python.org/packages/source/v/virtualenv/virtualenv-15.0.0.tar.gz && \
    tar -zxvf virtualenv-15.0.0.tar.gz && \
    cd virtualenv-15.0.0 && \
    $LOC/python-2.7.11/bin/python setup.py install && \
    cd $LOC && \
    rm -Rf virtualenv-15.0.0.tar.gz && \
    rm -Rf virtualenv-15.0.0


# Install HMMER and Easel
RUN \
    cd $LOC && \
    curl -OL http://eddylab.org/software/hmmer3/3.1b2/hmmer-3.1b2.tar.gz && \
    tar zxf hmmer-3.1b2.tar.gz && \
    cd hmmer-3.1b2 && \
    ./configure --prefix=$LOC/hmmer-3.1b2 && \
    make && \
    make install && \
    cd easel && \
    make install && \
    cd $LOC && \
    rm hmmer-3.1b2.tar.gz

# Install Rscape
RUN \
    cd $LOC && \
    curl -OL http://eddylab.org/software/rscape/rscape_v0.3.3.tar.gz && \
    tar zxf rscape_v0.3.3.tar.gz && \
    cd rscape_v0.3.3 && \
    ./configure --prefix=$LOC/rscape_v0.3.3 && \
    make && \
    make install && \
    cd $LOC && \
    rm rscape_v0.3.3.tar.gz

# Install RNAcode
RUN \
    cd $LOC && \
    curl -OL http://github.com/downloads/wash/rnacode/RNAcode-0.3.tar.gz && \
    tar zxf RNAcode-0.3.tar.gz && \
    cd RNAcode-0.3 && \
    ./configure --prefix=$LOC/RNAcode-0.3 && \
    make && \
    make install && \
    cd $LOC && \
    rm RNAcode-0.3.tar.gz

# Create autoRfam virtual environment
ADD requirements.txt $LOC
#   Dockerfile reference:
#   in ADD <src> <dest>, the <src> path must be inside the context of the build" !!
RUN \
    cd $LOC && \
    $LOC/python-2.7.11/bin/virtualenv venv-autorfam --python=$LOC/python-2.7.11/bin/python && \
    source $LOC/venv-autorfam/bin/activate && \
    cd $RUT && ls && \
    pip install -r $LOC/requirements.txt


# Start up
ENTRYPOINT \
    bin/bash
