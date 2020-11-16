# From the Kali linux base image
FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && apt-get clean all
RUN apt-get install -y kali-linux-default && apt-get clean all

RUN apt-get update && apt-get install -y \
	 iputils-ping \
     gobuster \
	 python-pip \ 
	 python3-pip

# Golismero
RUN git clone https://github.com/golismero/golismero /usr/share/golismero
WORKDIR /usr/share/golismero
RUN pip install -r requirements.txt
RUN pip install -r requirements_unix.txt
RUN ln -s /usr/share/golismero/golismero.py /usr/bin/golismero

# Finalrecon
RUN git clone https://github.com/thewhiteh4t/finalrecon.git /usr/share/finalrecon
WORKDIR /usr/share/finalrecon
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN sed -i "s/'requirements.txt'/'\/usr\/share\/finalrecon\/requirements.txt'/g" finalrecon.py 
RUN sed -i "s/'wordlists\/dirb_common.txt'/'\/usr\/share\/finalrecon\/wordlists\/dirb_common.txt'/g" finalrecon.py
RUN sed -i "s/os.getcwd()/'\/usr\/share\/finalrecon'/g" finalrecon.py
RUN ln -s /usr/share/finalrecon/finalrecon.py  /usr/bin/finalrecon
RUN chmod +x /usr/bin/finalrecon
RUN updatedb
WORKDIR /root




