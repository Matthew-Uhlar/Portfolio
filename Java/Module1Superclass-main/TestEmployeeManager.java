// Test class
public class TestEmployeeManager {
    public static void main(String[] args) {
        // Test Employee class
        Employee emp1 = new Employee();
        emp1.setFirstName("John");
        emp1.setLastName("Doe");
        emp1.setEmployeeID(1001);
        emp1.employeeSummary();
        
        // Test Manager class
        Manager manager1 = new Manager();
        manager1.setFirstName("Jane");
        manager1.setLastName("Smith");
        manager1.setEmployeeID(2001);
        manager1.setDepartment("HR");
        manager1.employeeSummary();
    }
}
