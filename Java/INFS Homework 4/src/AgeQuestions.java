import java.util.Scanner;

public class AgeQuestions {
	static String[] names = {"Buster", "Jill", "Pat", "Jenny", "Mason", "Bubba", "Howard"};
	static int[] ages = {8, 16, 18, 21, 25, 44, 44};
	  public static void main(String[] args) {
		  int ageCompare = 0;
		  char choice = '\0';
		  boolean FOUND = false;
		  
		  Scanner input = new Scanner(System.in);
		  
		  while (choice != 'X' || choice != 'x') {
			  
			  System.out.println("What would you like to do?");
			  System.out.println("1. View everyone younger than the inputed age.");
			  System.out.println("2. View everyone the same age as the inputed age.");
			  System.out.println("3. View everyone older than the inputed age.");
			  System.out.println("Please input the number you would like to do or X to exit.");
			  choice = input.next().charAt(0);
//			  System.out.println(choice);
			  	if (choice != '1' && choice != '2' && choice != '3' && choice != 'x' && choice != 'X') {
			  		System.out.println("Invalid Input");
			  	} else if (choice == 'X' || choice == 'x') {
			  		
			  		input.close();
			  		break;
			  		
			  	} else if (choice == '1' || choice == '2' || choice == '3'){
			  		System.out.println("Please input the age you would like to compare");
			  		ageCompare = input.nextInt();
			  		
			  		for (int i=0; i < 7; i++) {
			  			if (choice == '1') {
			  				if (ageCompare > ages[i]) {
			  					System.out.println(names[i] + " : " + ages[i] + " is younger than " + ageCompare);
			  					FOUND = true;
			  				}
			  			} else if (choice == '2') {
			  				if (ageCompare == ages[i]) {
			  					System.out.println(names[i] + " : " + ages[i] + " is equal " + ageCompare);
			  					FOUND = true;
			  				}
			  			} else if (choice == '3') {
			  				if (ageCompare < ages[i]) {
			  					System.out.println(names[i] + " : " + ages[i] + " is older than " + ageCompare);
			  					FOUND = true;
			  				}
			  			}
			  			
			  			
			  		}
			  		if (FOUND == false) {
			  				System.out.println(ageCompare + " not fount");
			  		}
			  	}
			  	
			}
		    
		  }
}
