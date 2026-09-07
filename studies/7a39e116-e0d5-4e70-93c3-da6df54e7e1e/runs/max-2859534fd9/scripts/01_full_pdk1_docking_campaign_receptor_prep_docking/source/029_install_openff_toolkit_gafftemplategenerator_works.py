
# Install openff-toolkit so GAFFTemplateGenerator works
result = __import__('subprocess').run(
    ["pip", "install", "openff-toolkit", "--quiet", "--no-deps"],
    capture_output=True, text=True, timeout=120
)
print("stdout:", result.stdout[:500])
print("stderr:", result.stderr[:500])
print("returncode:", result.returncode)
