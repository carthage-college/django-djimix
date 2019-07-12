django-djimix
=============

Tools for interacting with Informix

Informix Configuration Files
-------------------

In the settings file you will see ODBC connection strings whose first
arguments are "informix". This referes to the ODBC configurations described
below for Unix systems.

**/etc/odbcinst.ini**

```
[Informix]
Driver = /opt/ibm/informix/lib/cli/libifcli.so
APILevel=1
ConnectFunctions=YYY
DriverODBCVer=03.51
FileUsage=0
SQLLevel=1
smProcessPerConnect=Y
```

**/etc/odbc.ini**

```
[INFORMIX-PYTHON]
Driver = Informix
Server = servername
Port = 0000
User = xxx
Password = xxx
Database = databasename
```

**/opt/ibm/informix/etc/sqlhosts**

For the value of &quot;Server&quot; above, you must include that name in the
sqlhosts file like so:

```
#INFSERVER    COMPROT         HOSTNAME        PORTNAME
servername        onsoctcp        hostname          informix
```

The /etc/services entry for informix should look like this:

```
informix    18001/tcp           # informix
```

Python Code
==============

__Connecting via ODBC__

```
import pyodbc
cnxn = pyodbc.connect("DSN=MSSQL-PYTHON;UID=xxxx;PWD=xxxx")

cursor = cnxn.cursor()
# show tables
result     = connection.execute("exec sp_tables")

row = result.fetchone()
print row
```

**Client configuration on Informix server**

In the past, using a client-server architecture with IBM Informix database software required adding an entry on the database server with the client details, either in a .rhosts file in a specific user directory or the/etc/hosts.equiv file. If one of these was not present the client would receive an -956 error when attempting to connect to the server:

<pre>
listener-thread: err = -956: oserr = 0: errstr = client@clientmachine.company.com[clientmachine.company.com]: Client host or user client@clientmachine.company.com[clientmachine.company.com] is not trusted by the server.
</pre>

While .rhosts or /etc/hosts.equiv worked, it was often inconvenient to place a .rhosts file in the home directory of each user that needed to connect, and root prilivleges are usually required to add or edit a hosts.equiv in the /etc directory.

Starting in IBM Informix 11.70 and higher, IBM addressed this issue with a special configuration parameter that can be placed in $INFORMXIDIR/etc and is owned by the database server user (informix in most cases). The parameter is specified by REMOTE_SERVER_CFG in the onconfig file for an instance:

<pre>
REMOTE_SERVER_CFG trusted_clients.file
</pre>

The file can have any name you wish as long as it exists.

The format of the file is the same as hosts.equiv with a client hostname and user ID separated by white space:

<pre>
clientmachine.company.com  client
</pre>

<pre>
clientmachine.company.com  other_user
</pre>

The benefits of this mechanism are both the database administrator (DBA) having the ability to add and edit trusted client users without involving a system administrator, and the ability of the DBA to add the trusted user configuration file on the fly with onmode -wm:

<pre>
onmode -wm REMOTE_SERVER_CFG=trusted_clients.file
</pre>

Once executed, the above command will take immediate effect until the database server is stopped. To write the configuration parameter to the onconfig file permanently, use onmode -wf:

<pre>
onmode -wf REMOTE_SERVER_CFG=trusted_clients.file
</pre>
