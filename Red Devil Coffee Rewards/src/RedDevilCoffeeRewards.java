import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;

import javax.swing.*;

public class RedDevilCoffeeRewards {
	
	static int coffees = 0;
	
	public static void main(String[] args) {
		
		JFrame frame = new JFrame("Red Devil Coffee Rewards");
        JButton b = new JButton("Buy Coffee");
        b.setBounds(120,50,115,25);
        
        frame.add(b);
        frame.setSize(365,185);
        frame.setLayout(null);
        b.setHorizontalAlignment(SwingConstants.CENTER);
        
        JLabel numberOfCoffees = new JLabel();
        numberOfCoffees.setText("Number of coffees: " + coffees);
        numberOfCoffees.setBounds(119, 50, 130, 75);
        frame.add(numberOfCoffees);
        frame.setVisible(true);
        ImageIcon img = new ImageIcon("coffee_icon.jpg");
        frame.setIconImage(img.getImage());
        
		b.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent evt) {
				coffees++;
				numberOfCoffees.setText("Number of coffees: " + coffees);
				if(coffees >= 10) {
					try {
						PrintWriter pw = new PrintWriter(new FileOutputStream("coupon.txt"));
						pw.println("CONGRATULATIONS!");
						pw.println("");
						pw.println("With the purchase of your tenth coffee you have earned a free coffee!");
						pw.close();
					} catch (FileNotFoundException e) {
						e.printStackTrace();
					}
				}
			}
		});
	}
	
}
