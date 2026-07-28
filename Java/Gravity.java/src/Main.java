public class Main {
	
	public static double distanceFallen(double time,double gAcc) {
	      
	       return (0.5)*gAcc*Math.pow(time,2);
	   }
	   public static void main(String[] args) {
		      
	       System.out.printf("%5s%15s%15s\n","Time","Earth","Moon");
	      
	       for (int i = 0; i <= 10; i++) {
	          
	           System.out.printf("%5d%15.4fm%15.4fm\n",i,distanceFallen(i, 9.8),distanceFallen(i, 1.625));
	       }
	   }
}