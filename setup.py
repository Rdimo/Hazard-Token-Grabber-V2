import os

print("Installing requirements")
os.system(f"py -m pip install -r requirements.txt >nul")
    
print("Installed all requirements!")
print("Starting build-exe.bat...")

os.system("build-exe.bat")
