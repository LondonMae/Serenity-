import paramiko
client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect('10.25.5.234',username="turtlebot",password='turtlebot')
stdin, stdout, stderr = client.exec_command("cd catkin_ws \n ls \n source devel/setup.sh \n catkin_make \n roslaunch turtlebot_bringup minimal.launch --screen")
stdin.close()
for line in stdout.read().splitlines():
    print(line)
