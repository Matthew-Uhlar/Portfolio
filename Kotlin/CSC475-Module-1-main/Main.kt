import java.util.Scanner

fun main() {
    val scanner = Scanner(System.`in`)

    println("Welcome to Calculator")
    println("Choose an operation: +, -, *, /")
    val operation = scanner.next()

    println("Enter first number:")
    val num1 = scanner.nextDouble()

    println("Enter second number:")
    val num2 = scanner.nextDouble()

    val result = when (operation) {
        "+" -> num1 + num2
        "-" -> num1 - num2
        "*" -> num1 * num2
        "/" -> if (num2 != 0.0) num1 / num2 else "Error: Division by zero"
        else -> "Invalid operation"
    }

    println("Result: $result")
}
