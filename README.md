# Master Tool of Hacking

### Kali Linux in Windows with Docker

This tool was created to solve a problem, using Kali Linus directly from Windows with the help of Docker containers. (the principle was if it has a GUI probably exists a windows version for it) 

The application has two interfaces.

GUI: 

![image](https://user-images.githubusercontent.com/63077197/99310419-acbef080-2863-11eb-8f3b-71635ea5abbe.png)

Command line:

![image](https://user-images.githubusercontent.com/63077197/99310461-bcd6d000-2863-11eb-8ae0-2353b38f9e00.png)

The dockerfile contains the default kali linux metapackage and tools to which I added FinalRecon (https://github.com/thewhiteh4t/FinalRecon) and Golismero (https://github.com/golismero/golismero).

![image](https://user-images.githubusercontent.com/63077197/99311032-99f8eb80-2864-11eb-9205-19e34aa803a9.png)

At the user's need, it can open kali linux terminals and data persistance is kept with the help of docker volumes.

![image](https://user-images.githubusercontent.com/63077197/99311216-ee03d000-2864-11eb-96ed-6b632b5dc9ac.png)
