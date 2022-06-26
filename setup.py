import os

requirements = """httpx\npyotp\npsutil\npypiwin32\npycryptodome\npyinstaller>=4.9\nPIL-tools"""
for requirement in requirements.split("\n"):
    requirement = requirement.split(">")
    print("Installing {}".format(requirement[0]))
    os.system(f"py -m pip install {'>'.join(requirement)} >nul")
    
print("Installed all requirements!")
print("Starting build-exe.bat...")

os.system("build-exe.bat")
