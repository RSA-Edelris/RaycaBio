
# Examine activity column and key fields
print("HIT P841 values:")
print(df['HIT P841'].value_counts())
print()
print("Hit_rank values:")
print(df['Hit_rank'].value_counts().head(10))
print()
print("Stereo  Configuration sample:")
print(df['Stereo  Configuration'].value_counts().head(10))
print()
print("AS ratio sample (first 5):", df['AS ratio'].head().tolist())
print("RTmin sample (first 5):", df['RTmin'].head().tolist())
