package homeWork3.java;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Scanner;

public class homeWork3 {
	public static void main(String[] args) throws FileNotFoundException {
		ArrayList<Integer> ages = new ArrayList<Integer>();
		ArrayList<String> names = new ArrayList<String>();
		boolean yn = true;
		int position = 0;
		String decision = "";
		String file = "";
	
		Scanner input = new Scanner(System.in);
		Scanner input2 = new Scanner(System.in);
		
		while (yn) {
			System.out.println("Please enter a name:");
			names.add(input.next());
			System.out.println("Please enter an age:");
			ages.add(input.nextInt());
			System.out.println("Would you like to enter an additional record?");
			decision = input2.nextLine();
			
			switch(decision)
			{
	        case "yes":
	            yn = true;
	            break;

	        case "no":
	            yn = false;
	            break;

	        default:
	            System.out.println("please enter again ");
	            boolean repeat = true;

	            while (repeat)
	            {
	                System.out.println("Would you like to enter an additional record?");
	                decision = input2.nextLine();

	                switch (decision)
	                {
	                    case "yes":
	                        yn = true;
	                        repeat = false;
	                        break;

	                    case "no":
	                        yn = repeat = false;
	                        break;
	                    default:
	                        repeat = true;
	                }
	            }
	            break;
	    }

				

			}
		for (String i : names) {
		      System.out.println("Name " + i);
		      System.out.println("Age " + ages.get(position));
		      position++;
		}
		System.out.println("Would you like to save these to a file?");
		file = input2.nextLine();
		String yes = "yes";
		String Yes = "Yes";
		if (file.equals(yes) || file.equals(Yes)) {
			System.out.println("What would you like to name the file?");
			String fileName = input2.nextLine();
			PrintWriter pw = new PrintWriter(new FileOutputStream(fileName));
			position = 0;
			    for (String x : names) {
			        pw.println("Name: " + x +" - Age: " + ages.get(position));
				    position++;
				}
			    pw.close();
		} else if(!file.equals(yes) && !file.equals(Yes)) {
			System.out.println("Thanks for playing!");
		}
	input.close();
	input2.close();
	
	}
}


