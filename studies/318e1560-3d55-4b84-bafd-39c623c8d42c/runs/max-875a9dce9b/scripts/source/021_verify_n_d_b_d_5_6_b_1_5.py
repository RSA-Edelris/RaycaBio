
import numpy as np

# Verify n* = d²/b² for d=5.6, b=1.5
d = 5.6
b = 1.5
n_star = (d/b)**2
print(f"n* = ({d}/{b})^2 = {n_star:.4f}")
print(f"n* rounded to 1 dp = {n_star:.1f}")
print()

# What d gives n*=13.8?
n_star_claimed = 13.8
d_needed = np.sqrt(n_star_claimed * b**2)
print(f"d needed for n*=13.8: {d_needed:.4f} Å  (rounds to {d_needed:.1f})")

# What d gives n*=13.9?
n_star_alt = 13.9
d_needed_alt = np.sqrt(n_star_alt * b**2)
print(f"d needed for n*=13.9: {d_needed_alt:.4f} Å  (rounds to {d_needed_alt:.1f})")
