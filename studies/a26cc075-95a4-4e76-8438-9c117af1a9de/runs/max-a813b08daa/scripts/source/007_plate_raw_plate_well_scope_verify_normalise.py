
# plate_raw and plate_well are in scope — verify then normalise
plate_max  = plate_raw.max()
plate_norm = plate_raw / plate_max

print(f"plate_max: {plate_max:.4f}")
print(f"range:     {plate_norm.min():.3f} – {plate_norm.max():.3f}")
print("row 0 wells:", plate_well[0])
print("row 5 wells:", plate_well[5])     # DMCyDA row
