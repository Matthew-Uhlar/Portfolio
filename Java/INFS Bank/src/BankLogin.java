	import javax.swing.*;
	import java.awt.event.*;
	
	public class BankLogin implements ActionListener{
	    //instance variables
	    JFrame f;
	    JTextField text1, text2;
	    JButton button3;
	    JLabel label1, label2;
	    String username = "uccs";
	    int password = 1234;

	    BankLogin() {
	        f = new JFrame("ACME Bank Login");
	        text1 = new JTextField();
	        text1.setBounds(130, 60, 120, 20);
	        label1 = new JLabel("Username:", SwingConstants.RIGHT);
	        label1.setBounds(15, 60, 100, 20);
	        label1.setAlignmentX(100);
	        label2 = new JLabel("Pin:", SwingConstants.RIGHT);
	        label2.setBounds(15, 110, 100, 20);
	        text2 = new JTextField();
	        text2.setBounds(130, 110, 120, 20);

	        button3 = new JButton("Submit");
	        button3.setBounds(300, 80, 80, 20);

	        button3.addActionListener(this);
	        
	        f.add(text1);
	        f.add(label1);
	        f.add(text2);
	        f.add(label2);
	        f.add(button3);
	        f.setLayout(null);
	        f.setSize(400, 400);
	        f.setBounds(100, 100, 435, 230);
	        f.setVisible(true);
	        f.setResizable(false);
	        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	    }

	    @Override
	    public void actionPerformed(ActionEvent e) {
	    	try {
	    		int pin = Integer.parseInt(text2.getText());
	        if (e.getSource() == button3) {
	            	if (text1.getText().equals(username) && pin == password) {
	            		new ACMEBank();
	            		f.setVisible(false);
	            	} else{
	            		JOptionPane.showMessageDialog(f, "<html><span style = 'color:red'>Incorrect Username/Password!</span></html>");
	            	}
	        }
	    	}
	       catch(NumberFormatException ee){
	    	   JOptionPane.showMessageDialog(f, "<html><span style = 'color:red'>Please input valid characters.</span></html>");
	       }
	          	
	    }

	    
}
