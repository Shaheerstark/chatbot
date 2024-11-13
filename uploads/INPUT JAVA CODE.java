import java.util.Scanner;

public class FibonacciSeries {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Input the number of terms
        System.out.print("Enter the number of terms: ");
        int n = scanner.nextInt();

        // Initialize the first two terms of the Fibonacci series
        int first = 0, second = 1;

        System.out.println("Fibonacci Series:");

        for (int i = 1; i <= n; i++) {
            System.out.print(first + " ");

            // Calculate the next term
            int next = first + second;
            first = second;
            second = next;
        }

        scanner.close();
    }
}

