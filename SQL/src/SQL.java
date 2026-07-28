import java.awt.Font;
import java.sql.*;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.SwingConstants;

public class SQL {	 
	
	JFrame f;
	JLabel label1, label2, label3;
	Connection connection = null;
	int sum = 0;
	int exp = 0;
	int profit = sum - exp;
	
	SQL() {
	
    try {
   	 
   	 String serverName = "128.198.162.204";
   	 
   	 String schema = "INFS3070";
   	 
   	 String url = "jdbc:mysql://" + serverName +  "/" + schema;
//   	 System.out.println(url);
   	 
   	 String username = "infsclass";
   	 
   	 String password = "webclass";
   	 
   	 connection = DriverManager.getConnection(url, username, password);
   	 
   	 System.out.println("Successfully Connected to the database!");
    }
   	  

   	 catch (SQLException e) {
 
   	 	System.out.println("Could not connect to the database " + e.getMessage());
   	 	
    }
    
    Statement salesStatement;
	try {
		salesStatement = connection.createStatement();
		ResultSet res = salesStatement.executeQuery("SELECT SUM(Weekly_Sales) FROM SALES");
		while (res.next()){
			  int c = res.getInt(1);
			  sum = sum+c;
			  }
    
	} catch (SQLException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	Statement expenseStatement;
	try {
		expenseStatement = connection.createStatement();
		ResultSet res = expenseStatement.executeQuery("SELECT SUM(Amount) FROM EXPENSES");
		while (res.next()){
			  int c = res.getInt(1);
			  exp = exp+c;
			  }
    
	} catch (SQLException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
    
    

		 f = new JFrame("SQL");
	     label1 = new JLabel("Sales: $" + sum, SwingConstants.LEFT);
	     label1.setBounds(60, 70, 100, 20);
	     label1.setAlignmentX(100);
	     label2 = new JLabel("Expenses: $" + exp, SwingConstants.LEFT);
	     label2.setBounds(60, 120, 100, 20);
	     label3 = new JLabel("Profit: $" + profit, SwingConstants.LEFT);
	     label3.setBounds(60, 170, 100, 20);
	     
	     label1.setFont(new Font("Tahoma", Font.PLAIN, 12));
	     label2.setFont(new Font("Tahoma", Font.PLAIN, 12));
	     label3.setFont(new Font("Tahoma", Font.PLAIN, 12));
		 
	     f.add(label2);
	     f.add(label3);
	     f.add(label1);
		 
		 f.setLayout(null);
	     f.setSize(400, 400);
	     f.setBounds(100, 100, 400, 300);
	     f.setVisible(true);
	     f.setResizable(false);
	     f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	     
	     
	     

	     
	 }
	public static void main(String[] args) {
		new SQL();
	}
}
