import sys
print("=" * 50)
print("VisionBox Python Enviroment")
print("=" * 50)

print(f"\nPython executable:\n{sys.executable}")
print(f"\nPython version:\n{sys.version}")
print("\nSearch paths:")
for path in sys.path:
    print(f" - {path}")