import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify, symbols, lambdify

def regula_falsi_method():
    function_input = input("Masukkan fungsi (contoh: x**7 - 7*x + 7): ")
    lower_bound = float(input("Masukkan batas bawah (a): "))
    upper_bound = float(input("Masukkan batas atas (b): "))
    tolerance = float(input("Masukkan toleransi error (contoh: 1e-7 atau 0.0007): "))
    max_iterations = int(input("Masukkan maksimum iterasi: "))

    # Convert input into a mathematical function
    x = symbols('x')
    expression = sympify(function_input)
    function = lambdify(x, expression, 'numpy')

    # Validate the interval
    if function(lower_bound) * function(upper_bound) >= 0:
        print("Metode gagal: Tidak ada perubahan tanda di interval tersebut.")
        return

    # Display table header
    print("\n" + "=" * 60)
    print(f"{'Iterasi':<8} | {'a':<10} | {'b':<10} | {'c':<10} | {'f(c)':<10}")
    print("=" * 60)

    # Initialize graph
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))

    x_values = np.linspace(lower_bound - 1, upper_bound + 1, 400)
    y_values = function(x_values)

    previous_c = lower_bound

    # Iteration process
    for iteration in range(1, max_iterations + 1):
        f_lower = function(lower_bound)
        f_upper = function(upper_bound)

        # Calculate the Regula Falsi approximation
        c = (lower_bound * f_upper - upper_bound * f_lower) / (f_upper - f_lower)
        f_c = function(c)

        # Display iteration results
        print(f"{iteration:<8} | {lower_bound:<10.6f} | {upper_bound:<10.6f} | {c:<10.6f} | {f_c:<10.6f}")

        # Update graph visualization
        ax.clear()
        ax.plot(x_values, y_values, label=f'f(x) = {function_input}')
        ax.axhline(0)

        # Draw secant line
        ax.plot([lower_bound, upper_bound], [f_lower, f_upper], 'r--', alpha=0.6, label="Garis Secant")

        # Mark root approximation
        ax.scatter(c, f_c, label=f'c = {c:.4f}', zorder=5)

        ax.set_title(f"Iterasi {iteration}")
        ax.legend()
        ax.grid()

        plt.draw()
        plt.pause(0.8)

        # Check stopping conditions
        if abs(f_c) < tolerance or abs(c - previous_c) < tolerance:
            print("=" * 60)
            print(f"Akar ditemukan: x = {c:.8f}")
            break

        previous_c = c

        # Update interval boundaries
        if f_lower * f_c < 0:
            upper_bound = c
        else:
            lower_bound = c

    plt.ioff()
    plt.show()

# Main program
if __name__ == "__main__":
    regula_falsi_method()