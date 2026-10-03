// Manager class
public class Manager extends Employee {
    private String department;

    // Getters and Setters for department
    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    // Overriding employeeSummary method to include subclass attributes
    @Override
    public void employeeSummary() {
        super.employeeSummary();
        System.out.println("Department: " + department);
    }
}
