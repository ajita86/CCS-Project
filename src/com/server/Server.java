package com.server;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {

	public static void main(String[] args) throws Exception {
		
		System.out.println("S : Server has started...");
		ServerSocket socServer = new ServerSocket(9999);
		System.out.println("S : Waiting for a client request...");
		Socket s = socServer.accept();
		System.out.println("S : Client connected");
		
		BufferedReader br = new BufferedReader(new InputStreamReader(s.getInputStream()));
		String str = br.readLine();
		System.out.println("S : Client data: " + str);
		
		String nickname = str.substring(0, 2);
		OutputStreamWriter os = new OutputStreamWriter(s.getOutputStream());
		PrintWriter out = new PrintWriter(os);
		out.println(nickname);
		out.flush();

	}

}
