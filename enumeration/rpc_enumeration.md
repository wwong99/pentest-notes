# RPC Enumeration (Remote Procedure Call)

## Connect to an RPC share without a username and password and enumerate privileges

```ShellSession
rpcclient --user="" --command=enumprivs -N $ip
```

## Connect to an RPC share with a username and enumerate privileges

```ShellSession
rpcclient --user="" --command=enumprivs $ip
```
