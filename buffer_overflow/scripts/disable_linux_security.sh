cat /proc/sys/kernel/randomize_va_space
sudo bash -c 'echo "kernel.randomize_va_space = 0" >> /etc/sysctl.conf'
sudo sysctl -p
cat /proc/sys/kernel/randomize_va_space
# verify "0"
ulimit -c unlimited
ulimit -c
