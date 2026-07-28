// ShapeArray.java
public class ShapeArray {
    public static void main(String[] args) {
        Shape[] shapeArray = new Shape[3];

        shapeArray[0] = new Triangle(3, 4, 5);
        shapeArray[1] = new Circle(5);
        shapeArray[2] = new Rectangle(4, 5);

        for (Shape shape : shapeArray) {
            System.out.println(shape);
        }
    }
}
