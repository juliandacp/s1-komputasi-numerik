import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Function to be integrated
def f(x):
    return np.exp(x) * np.sin(x)

# Trapezoidal rule
def trapezoidal(f, a, b, n):
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))

    for i in range(1, n):
        total += f(a + i * h)

    return total * h

# Romberg integration
def romberg(f, a, b, max_level):
    R = np.zeros((max_level, max_level))

    # R(i, 0) = Trapezoidal rule with 2^i intervals
    for i in range(max_level):
        n = 2**i
        R[i, 0] = trapezoidal(f, a, b, n)

    # Richardson extrapolation
    for j in range(1, max_level):
        for i in range(j, max_level):
            R[i, j] = R[i, j - 1] + (R[i, j - 1] - R[i - 1, j - 1]) / (4**j - 1)

    return R

# Main output
def main():
    a = 0.0
    b = 3.0
    max_level = 6

    # Calculate the exact integral value
    exact_value, _ = quad(f, a, b)

    # Romberg table calculation
    R = romberg(f, a, b, max_level)

    # Calculate errors
    trapezoidal_error = [abs(R[i, 0] - exact_value) for i in range(max_level)]
    romberg_error = [abs(R[i, i] - exact_value) for i in range(max_level)]

    interval_count = [2**i for i in range(max_level)]

    # Display exact integral value
    print("=" * 80)
    print(f"Hasil Integral Eksak : {exact_value:.10f}")
    print("=" * 80)

    # Trapezoidal table
    print("\nTABEL HASIL TRAPEZOIDAL")
    print("-" * 40)
    print(f"{'Orde':<5} | {'n':<4} | {'Hasil Trapezoidal'}")
    print("-" * 40)

    for i in range(max_level):
        print(f"{i:<5} | {interval_count[i]:<4} | {R[i, 0]:.10f}")

    # Romberg table
    print("\nTABEL MATRIKS ROMBERG")
    print("Dengan Ekstrapolasi Richardson")
    print("-" * 90)

    for i in range(max_level):
        row = f"Orde {i} (n = {interval_count[i]:2}): "

        for j in range(i + 1):
            row += f"{R[i, j]:14.10f} "

        print(row)

    # Error comparison table
    print("\nTABEL PERBANDINGAN ERROR PER ORDE")
    print("-" * 65)
    print(f"{'Orde':<5} | {'n':<4} | {'Error Trapezoidal':<20} | {'Error Romberg'}")
    print("-" * 65)

    for i in range(max_level):
        print(f"{i:<5} | {interval_count[i]:<4} | {trapezoidal_error[i]:<20.10f} | {romberg_error[i]:.10f}")

    print("-" * 65)

    # Error comparison graph
    plt.figure(figsize=(8, 5))

    plt.plot(interval_count, trapezoidal_error, marker='o', linestyle='-', color='red', label='Error Trapezoidal')
    plt.plot(interval_count, romberg_error, marker='s', linestyle='-', color='blue', label='Error Romberg')

    plt.yscale('log')
    plt.xlabel('Jumlah Pias / Interval (n)')
    plt.ylabel('Galat Absolut (Log Scale)')
    plt.title('Perbandingan Penurunan Galat: Trapezoidal vs Romberg')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()