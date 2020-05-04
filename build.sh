docker build -t iox-ir1101-serial-port . && \
ioxclient docker package iox-ir1101-serial-port . -n iox-ir1101-serial-port-`date +"%Y%m%d-%H%M%S"`
