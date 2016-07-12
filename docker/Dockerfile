FROM fedora
MAINTAINER loadtheaccumulator@gmail.com
RUN dnf install -y git
RUN dnf install -y python-pip
RUN pip install --upgrade pip
RUN pip install --upgrade git+git://github.com/loadtheaccumulator/glusto.git
RUN mkdir /etc/glusto/
COPY defaults/defaults.yml /etc/glusto/
