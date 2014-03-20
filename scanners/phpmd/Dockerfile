FROM ubuntu
ENV HOME /root
RUN apt-get update
RUN apt-get install -y php5-cli php-pear
RUN pear channel-discover pear.phpmd.org
RUN pear channel-discover pear.pdepend.org
RUN pear install --alldeps phpmd/PHP_PMD
