import javax.swing.*;
import java.awt.event.*;

public class ACMEBank implements ActionListener {

    //instance variables
    JFrame f;
    JTextField text1, text2, text3;
    JButton button1, button2, button3;
    JLabel label1, label2, label3, label4;
    double balance;

    ACMEBank() {
        balance = 0.0;
        f = new JFrame("ACME Bank");
        text1 = new JTextField();
        text1.setBounds(130, 10, 120, 20);
        label1 = new JLabel("Credit", SwingConstants.RIGHT);
        label1.setBounds(15, 10, 100, 20);
        label1.setAlignmentX(100);
        label2 = new JLabel("Debit", SwingConstants.RIGHT);
        label2.setBounds(15, 60, 100, 20);
        text2 = new JTextField();
        text2.setBounds(130, 60, 120, 20);

        button1 = new JButton("Credit");
        button1.setBounds(275, 10, 80, 20);
        
        button2 = new JButton("Debit");
        button2.setBounds(275, 60, 80, 20);

        button3 = new JButton("Clear");
        button3.setBounds(375, 30, 80, 20);
        
        label3 = new JLabel("Balance: ", SwingConstants.RIGHT);
        label3.setBounds(60, 105, 140, 20);
        label4 = new JLabel("$" + balance);
        label4.setBounds(210, 105, 150, 20);

        button1.addActionListener(this);
        button2.addActionListener(this);
        button3.addActionListener(this);
        
        f.add(text1);
        f.add(label1);
        f.add(text2);
        f.add(label2);

        f.add(label3);
        f.add(label4);
        f.add(button1);
        f.add(button2);
        f.add(button3);
        f.setLayout(null);
        f.setSize(400, 400);
        f.setBounds(100, 100, 470, 300);
        f.setVisible(true);
        f.setResizable(false);
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    @Override
    public void actionPerformed(ActionEvent e) {

        if (e.getSource() == button1) {

            try {
                double amount = Double.parseDouble(text1.getText());
                balance += amount;
                label4.setText("$" + balance);

            } catch (NumberFormatException ee) {
                JOptionPane.showMessageDialog(f, "Please only use numbers");
            }
        } else if (e.getSource() == button2) {
            try {
                double amount = Double.parseDouble(text2.getText());

                balance -= amount;
                label4.setText("$" + balance);

            } catch (NumberFormatException ee) {
                JOptionPane.showMessageDialog(f, "Please only use numbers");
            }
        } else if (e.getSource() == button3) {
            text1.setText("");
            text2.setText("");
        }
    }

    public static void main(String[] args) {
        new ACMEBank();
    }
}
