package info.shifvb.hash_calculator_java_swing;

import java.awt.EventQueue;

import javax.swing.ButtonGroup;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

import java.awt.BorderLayout;

import javax.swing.JButton;
import javax.swing.JTextField;
import javax.swing.JLabel;

import java.awt.Toolkit;

import javax.swing.JRadioButton;
import javax.swing.JTextArea;

import java.awt.datatransfer.StringSelection;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.MouseEvent;
import java.io.File;
import java.io.IOException;
import java.security.NoSuchAlgorithmException;

import javax.swing.JScrollPane;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;

public class HashCalculator {

	// language = 0 : simplefied Chinese
	// language = 1 : english
	public static int Language = 0;
	private JFrame frame;
	private JTextField textField;
	private JRadioButton rdbtnMd;
	private JRadioButton rdbtnSha;
	private JRadioButton rdbtnSha_1;
	private JRadioButton rdbtnSha_2;
	private JButton btnNewButton;
	private JTextArea textArea;
	private JLabel label;
	private JLabel label_1;
	private JButton button_2;
	private JButton button;
	private JButton button_1;
	private JMenuItem menuItem_2;
	private JMenu mno;
	private JMenuItem menuItem;
	private JMenuItem menuItem_1;
	private JMenu mnl;
	private JMenu mnh;
	private JMenuItem menuItem_3;
	private JMenuItem mntmEnglish;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					HashCalculator window = new HashCalculator();
					window.frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public HashCalculator() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		try {
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (ClassNotFoundException | InstantiationException
				| IllegalAccessException | UnsupportedLookAndFeelException e) {
			e.printStackTrace();
		}
		frame = new JFrame();
		frame.setResizable(false);
		frame.setBounds(100, 100, 482, 329);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setTitle("散列值计算器");

		JPanel panel_2 = new JPanel();
		frame.getContentPane().add(panel_2, BorderLayout.CENTER);
		panel_2.setLayout(null);

		label = new JLabel("\u6587\u4EF6\uFF1A");
		label.setBounds(28, 24, 46, 14);
		panel_2.add(label);

		textField = new JTextField();
		textField.setBounds(84, 21, 262, 20);
		panel_2.add(textField);
		textField.setColumns(10);

		button_2 = new JButton("\u6D4F\u89C8...");
		button_2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JFileChooser fc = new JFileChooser();
				fc.setFileSelectionMode(JFileChooser.FILES_ONLY);
				fc.setDialogTitle("请选择文件");
				fc.setApproveButtonText("确定(O)");
				fc.showOpenDialog(frame);
				File file = fc.getSelectedFile();
				if (file == null) {
					return;
				}
				String path = file.getPath();
				textField.setText(path);
			}
		});
		button_2.setBounds(356, 20, 89, 23);
		panel_2.add(button_2);

		rdbtnMd = new JRadioButton("md5");
		rdbtnMd.setBounds(28, 68, 74, 23);
		rdbtnMd.setSelected(true);
		panel_2.add(rdbtnMd);

		rdbtnSha = new JRadioButton("sha1");
		rdbtnSha.setBounds(128, 68, 74, 23);
		panel_2.add(rdbtnSha);

		rdbtnSha_1 = new JRadioButton("sha-256");
		rdbtnSha_1.setBounds(223, 68, 74, 23);
		panel_2.add(rdbtnSha_1);

		rdbtnSha_2 = new JRadioButton("sha-512");
		rdbtnSha_2.setBounds(327, 68, 74, 23);
		panel_2.add(rdbtnSha_2);

		label_1 = new JLabel("\u503C\uFF1A");
		label_1.setBounds(28, 119, 46, 14);
		panel_2.add(label_1);

		button_1 = new JButton("\u8BA1\u7B97\u6563\u5217\u503C");
		button_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if (textField.getText().equals("")) {
					if (HashCalculator.Language == 0) {
						JOptionPane.showMessageDialog(frame, "请选择文件！", "信息",
								JOptionPane.INFORMATION_MESSAGE);
					} else if (HashCalculator.Language == 1) {
						JOptionPane.showMessageDialog(frame,
								"Please select file!", "info",
								JOptionPane.INFORMATION_MESSAGE);
					}

					return;
				}
				String algorithm = null;
				// check algorithm
				if (rdbtnMd.isSelected()) {
					algorithm = "md5";
				}
				if (rdbtnSha.isSelected()) {
					algorithm = "sha1";
				}
				if (rdbtnSha_1.isSelected()) {
					algorithm = "sha-256";
				}
				if (rdbtnSha_2.isSelected()) {
					algorithm = "sha-512";
				}
				if (algorithm == null) {
					return;
				}
				try {
					textArea.setText(Hash.fileHash(
							new File(textField.getText()), algorithm));
				} catch (NoSuchAlgorithmException | IOException e1) {
					if (HashCalculator.Language == 0) {
						JOptionPane.showMessageDialog(frame, "文件不存在！", "信息",
								JOptionPane.INFORMATION_MESSAGE);
					} else if (HashCalculator.Language == 1) {
						JOptionPane.showMessageDialog(frame, "No such file!",
								"info", JOptionPane.INFORMATION_MESSAGE);
					}
				}
			}
		});
		button_1.setBounds(356, 115, 87, 23);
		panel_2.add(button_1);

		// button group
		ButtonGroup bg = new ButtonGroup();
		bg.add(rdbtnMd);
		bg.add(rdbtnSha);
		bg.add(rdbtnSha_1);
		bg.add(rdbtnSha_2);

		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setBounds(85, 113, 263, 105);
		panel_2.add(scrollPane);

		textArea = new JTextArea();
		textArea.setEditable(false);
		textArea.setLineWrap(true);
		scrollPane.setViewportView(textArea);

		JPanel panel_1 = new JPanel();
		panel_1.setBounds(0, 229, 476, 51);
		panel_2.add(panel_1);

		btnNewButton = new JButton("\u62F7\u8D1D\u5230\u526A\u5207\u677F");
		btnNewButton.setBounds(82, 11, 122, 29);
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				StringSelection ss = new StringSelection(textArea.getText());
				Toolkit.getDefaultToolkit().getSystemClipboard()
						.setContents(ss, ss);
			}
		});
		panel_1.setLayout(null);
		panel_1.add(btnNewButton);

		button = new JButton("\u9000\u51FA");
		button.setBounds(265, 11, 122, 29);
		button.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
			}
		});
		panel_1.add(button);

		JMenuBar menuBar = new JMenuBar();
		frame.setJMenuBar(menuBar);

		mno = new JMenu("\u6587\u4EF6(F)");
		mno.setMnemonic('O');
		menuBar.add(mno);

		menuItem = new JMenuItem("\u6253\u5F00");
		menuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				MouseEvent pevent = new MouseEvent(button_2,
						MouseEvent.MOUSE_PRESSED, 0, MouseEvent.BUTTON1_MASK,
						1, 1, 1, false);
				MouseEvent revent = new MouseEvent(button_2,
						MouseEvent.MOUSE_RELEASED, 0, MouseEvent.BUTTON1_MASK,
						1, 1, 1, false);
				EventQueue eq = Toolkit.getDefaultToolkit()
						.getSystemEventQueue();
				eq.postEvent(pevent);
				eq.postEvent(revent);
			}
		});
		mno.add(menuItem);

		menuItem_1 = new JMenuItem("\u9000\u51FA");
		menuItem_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
			}
		});
		mno.add(menuItem_1);

		mnl = new JMenu("Language(L)");
		mnl.setMnemonic('O');
		menuBar.add(mnl);

		menuItem_2 = new JMenuItem("\u7B80\u4F53\u4E2D\u6587");
		menuItem_2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				HashCalculator.Language = 0;
				frame.setTitle("散列值计算器");
				label.setText("文件：");
				button_2.setText("浏览...");
				label_1.setText("值：");
				button_1.setText("计算散列值");
				btnNewButton.setText("拷贝到剪切板");
				button.setText("退出");
				mno.setText("文件(F)");
				menuItem.setText("打开");
				menuItem_1.setText("退出");
				mnl.setText("Language(L)");
				mnh.setText("关于(H)");
				menuItem_3.setText("关于作者");
			}
		});
		mnl.add(menuItem_2);

		mntmEnglish = new JMenuItem("English");
		mntmEnglish.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				HashCalculator.Language = 1;
				frame.setTitle("Hash Calculator");
				label.setText("file:");
				button_2.setText("open...");
				label_1.setText("value:");
				button_1.setText("calculate");
				btnNewButton.setText("copy to clipboard");
				button.setText("exit");
				mno.setText("File(F)");
				menuItem.setText("Open");
				menuItem_1.setText("Exit");
				mnl.setText("Language(L)");
				mnh.setText("About(H)");
				menuItem_3.setText("About Writer");
			}
		});
		mnl.add(mntmEnglish);

		mnh = new JMenu("\u5173\u4E8E(H)");
		mnh.setMnemonic('H');
		menuBar.add(mnh);

		menuItem_3 = new JMenuItem("\u5173\u4E8E\u4F5C\u8005");
		menuItem_3.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JOptionPane
						.showMessageDialog(
								frame,
								"shifvb\ne-mail: shifvb@gmail.com\nAll rights reserved.",
								"About Writer", JOptionPane.INFORMATION_MESSAGE);
			}
		});
		mnh.add(menuItem_3);
	}
}
