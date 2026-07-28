import java.util.Formatter;
public class Gravity {
	static double distanceEarth;
	static double distanceMoon;
	static double ge = 9.8;
	static double gm = 1.625;
	static double d;
	static int t = 1;
	
	static void distanceFallen(int x, double y) {
		d = 0.5*y*(x*x);
	}
	
	public static void main (String[] args) {
		System.out.printf("%s %20s %20s \n", "Time", "Distance Earth", "Distance Moon");
		
		for(int i = 0; i < 10; i++) {
			distanceFallen(t, ge);
			distanceEarth = d;
			distanceFallen(t, gm);
			distanceMoon = d;
			System.out.1printf("%-2d %20f %20f \n", t, distanceEarth, distanceMoon);
			t++;
		}

	}
}
