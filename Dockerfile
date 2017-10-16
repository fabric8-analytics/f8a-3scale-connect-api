FROM registry.centos.org/centos/centos:7
MAINTAINER Arunkumar Srisailapathi <asrisail@redhat.com>

RUN useradd 3scale
# python3-pycurl is needed for Amazon SQS (boto lib), we need CentOS' rpm - installing it from pip results in NSS errors
RUN yum install -y gcc &&\
    yum install -y epel-release &&\
    yum install -y python34-pip &&\
    yum clean all

RUN mkdir -p /3scale
COPY ./ /3scale
WORKDIR /3scale
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]

