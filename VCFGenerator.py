import re
from datetime import datetime

class VCFGenerator:
    def __init__(self, input_path, output_path=""):
        self.input_file = input_path
        print(f"input path from VCF init: {self.input_file}")
        if output_path == "":
            self.output_file = self.generateFilename()
        else:
            self.output_file = output_path
        
    def cleanNumber(self, number):
        # Keep digits and leading +
        number = number.strip()
        if number.startswith("+"):
            return "+" + re.sub(r"\D", "", number)
        return re.sub(r"\D", "", number)

    def generateFilename(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"contacts {timestamp}.vcf"
    
    def generateVCF(self):
        # Using the built-in open() function with strings
        with open(self.input_file, "r", encoding="utf-8") as f, \
            open(self.output_file, "w", encoding="utf-8") as out:
            
            for i, line in enumerate(f, start=1):
                number = self.cleanNumber(line)
                if not number:
                    continue

                name = f"Contact {i:03d}"
                out.write(
                    "BEGIN:VCARD\n"
                    "VERSION:3.0\n"
                    f"N:{name};{name};;;\n"
                    f"FN:{name}\n"
                    f"TEL;TYPE=CELL:{number}\n"
                    "END:VCARD\n\n"
                )