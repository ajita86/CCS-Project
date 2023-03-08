package com.client;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class Client {

	public static void main(String[] args) throws Exception {
		
		String ip = "localhost";
		int port = 9999; // 0-1023 reserved 1024-65535 can be used
		Socket s = new Socket(ip, port);
		
		String str = "Ajita Shrivastava";
		
		OutputStreamWriter os = new OutputStreamWriter(s.getOutputStream());
		PrintWriter out = new PrintWriter(os);
		out.println(str);
		os.flush();
		
		BufferedReader br = new BufferedReader(new InputStreamReader(s.getInputStream()));
		String nickname = br.readLine();
		System.out.println("C : Server's response: " + nickname);
		
	}

}
