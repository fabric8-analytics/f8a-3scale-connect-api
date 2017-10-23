FROM registry.centos.org/centos/centos:7
MAINTAINER Arunkumar Srisailapathi <asrisail@redhat.com>

RUN useradd 3scale
# Install deps for cryptography:
#  https://cryptography.io/en/latest/installation/#rhel-centos
RUN yum install -y gcc &&\
    yum install -y epel-release &&\
    yum install -y python34-pip &&\
    yum install -y redhat-rpm-config gcc libffi-devel python34-devel openssl-devel &&\
    yum clean all

RUN mkdir -p /3scale
COPY ./ /3scale
WORKDIR /3scale
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]

