FROM mysql/mysql-server:5.7.19

# add backup scripts
ADD scripts/* /usr/local/bin/

# make them executable
RUN chmod +x /usr/local/bin/*

