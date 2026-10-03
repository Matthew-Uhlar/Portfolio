import java.util.Scanner;
public class RedDevilCoffeeRewards {
	static int beverages;
	static int overFour;
	static int overFourPoints;
	public static void main(String[] args) {
		
		Scanner input = new Scanner(System.in);
		
		System.out.println("Please enter the number of beverages purchased last week:");
		beverages = input.nextInt();
		
		if (beverages == 1) {
			System.out.println("You earned 5 points.");
		} else if (beverages == 2) {
			System.out.println("You earned 15 points.");
		} else if (beverages == 3) {
			System.out.println("You earned 30 points.");
		} else if (beverages > 3) {
			overFour = beverages - 3;
			overFourPoints = beverages * 20 + 30;
			System.out.println("You earned " + overFourPoints + " points.");
		}
		input.close();
	}
}
