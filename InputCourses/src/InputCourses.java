
import java.util.ArrayList;

public class InputCourses {
//	static String[] classes = {};
	static ArrayList<String> classes = new ArrayList<String>();
	static String exit = "exit";
	static String Exit = "Exit";
	public static void main(String[] args) {
		String choice = "";
		Scanner input = new Scanner(System.in);
		System.out.println("Please enter your first class or exit at any time to stop:");
		choice = input.nextLine();
		
		while (!choice.equals(exit) && !choice.equals(Exit)) {
			System.out.println("Please input your next class:");
			choice = input.nextLine();
			if (choice != "exit" && choice != "Exit") {
//				System.out.println("The choice variable is " + choice);
				classes.add(choice);
			}
			
		}
		System.out.println("Your classes are:");
		for (String i : classes) {
			System.out.println(i);
			input.close();
		}
	}
	
	
}
