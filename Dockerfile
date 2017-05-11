# alias es AUTORFAM_VOL=/path/to/autorfam/code
# volume es ${AUTORFAM_VOL}:/autorfam/autorfam-code
#
#	autorfam/ ($RUT)
#	│
# 	├── local/ ($LOC)
#	│   ├── Infernal
#	│   ├── Python
#	│   ├── requirements.txt
#	│   ├── virtualenv
#	│   └── venv-autorfam
#	│
# 	└── autorfam-code/ (**VOL**)
#		├── requirements.txt
#	    └── ...


FROM centos:6.6

RUN yum install -y \
    curl \
    gcc \
    git \
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


# Install Infernal
RUN \
    cd $LOC && \
    curl -OL http://eddylab.org/infernal/infernal-1.1.1.tar.gz && \
    tar -xvzf infernal-1.1.1.tar.gz && \
    cd infernal-1.1.1 && \
    ./configure --prefix=$LOC/infernal-1.1.1 && \
    make && \
    make install && \
    cd easel && \
    make install && \
    cd $LOC && \
    rm infernal-1.1.1.tar.gz

# Create autoRfam virtual environment
ADD requirements.txt $LOC
#      Dockerfile reference: ADD <src>... <dest> 
#      "The <src> path must be inside the context of the build;" !!
RUN \
    cd $LOC && \
    $LOC/python-2.7.11/bin/virtualenv venv-autorfam --python=$LOC/python-2.7.11/bin/python && \
    source $LOC/venv-autorfam/bin/activate && \
    cd $RUT && ls && \
    pip install -r $LOC/requirements.txt


#CMD $LOC/python -h

ENTRYPOINT \
    bin/bash
  #source $LOC/venv-autorfam/bin/activate && \



