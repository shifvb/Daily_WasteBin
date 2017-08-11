package info.shifvb.hash_calculator_java_swing;

import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;

public class Hash {
	private Hash() {
	}

	/**
	 * hash byte[]
	 * 
	 * @param b
	 * @param algorithm
	 * @return hex String
	 * @throws NoSuchAlgorithmException
	 */
	public static String hash(byte[] b, final String algorithm)
			throws NoSuchAlgorithmException {
		char hex[] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
				'B', 'C', 'D', 'E', 'F' };
		MessageDigest mdInst = MessageDigest.getInstance(algorithm);
		mdInst.update(b);
		byte[] md = mdInst.digest();
		char[] hexString = new char[md.length * 2];
		int x = 0;
		for (int i = 0; i < md.length; i++) {
			hexString[x++] = hex[md[i] >>> 4 & 0xf];
			hexString[x++] = hex[md[i] & 0xf];
		}
		return String.valueOf(hexString);
	}

	/**
	 * hash String
	 * 
	 * @param s
	 * @param algorithm
	 * @return hex String
	 * @throws NoSuchAlgorithmException
	 */
	public static String hash(String s, final String algorithm)
			throws NoSuchAlgorithmException {
		return Hash.hash(s.getBytes(), algorithm);
	}

	/**
	 * file hash
	 * 
	 * @param f
	 * @param algorithm
	 * @return
	 * @throws IOException
	 * @throws NoSuchAlgorithmException
	 */
	public static String fileHash(File file, final String algorithm)
			throws IOException, NoSuchAlgorithmException {
		// check if file exists
		if (!(file.exists() && file.isFile())) {
			throw new FileNotFoundException();
		}
		// read data to buffer
		DataInputStream dis = new DataInputStream(new FileInputStream(file));
		int temp;
		ArrayList<Byte> buffer = new ArrayList<Byte>();
		while ((temp = dis.read()) != -1) {
			buffer.add(new Byte((byte) temp));
		}
		dis.close();
		// call method
		byte[] data = new byte[buffer.size()];
		for (int i = 0; i < buffer.size(); i++) {
			data[i] = buffer.get(i).byteValue();
		}
		return Hash.hash(data, algorithm);
	}
}
