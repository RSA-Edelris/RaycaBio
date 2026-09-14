
# Verify the rounding of 0.1095 in Python
import decimal

print(f"Python f-string 3dp of 0.1095: {0.1095:.3f}")
print(f"Exact float repr: {0.1095!r}")
print(f"As decimal: {decimal.Decimal(0.1095)}")

# What is 0.9065 - 0.7970 exactly?
diff_rounded = 0.9065 - 0.7970
print(f"\n0.9065 - 0.7970 (float): {diff_rounded!r}")
print(f"As decimal: {decimal.Decimal(diff_rounded)}")
print(f"3dp: {diff_rounded:.3f}")

# What is the exact raw diff?
diff_raw = 0.9064819812774658 - 0.7970460057258606
print(f"\nRaw diff: {diff_raw!r}")
print(f"As decimal: {decimal.Decimal(diff_raw)}")
print(f"3dp: {diff_raw:.3f}")

# Verify other deltas
print(f"\nΔconf:  {0.47777947783470154 - 0.4483930468559265:.3f} (stated: 0.029)")
print(f"Δptm:   {0.4550328850746155 - 0.42173317074775696:.3f} (stated: 0.033)")
print(f"Δiptm:  {0.3133130967617035 - 0.2734520137310028:.3f} (stated: 0.040)")
print(f"Δligand_iptm: {diff_raw:.3f} (stated: 0.110)")
