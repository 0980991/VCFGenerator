import re
from datetime import datetime
import csv

class VCFGenerator:
    def __init__(self, input_path, output_path=""):
        self.input_file = input_path
        if output_path == "":
            self.output_file = self.generateFilename()
        else:
            self.output_file = output_path
        
    def sanitizeNumber(self, number):
        # Keep digits and leading +
        number = number.strip()
        if number.startswith("+"):
            return "+" + re.sub(r"\D", "", number)
        return re.sub(r"\D", "", number)

    def generateFilename(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        return f"contacts {timestamp}.vcf"
    
    def generateVCF(self):
        # Using the built-in open() function with strings
        with open(self.input_file, "r", encoding="utf-8") as f, \
            open(self.output_file, "w", encoding="utf-8") as out:
                
            # Parse txt file
            if self.input_file.endswith(".txt"): 
                for i, line in enumerate(f, start=1):
                    number = self.sanitizeNumber(line)
                    if not number:
                        continue

                    name = f"Contact {i:04d}"
                    out.write(
                        "BEGIN:VCARD\n"
                        "VERSION:3.0\n"
                        f"N:{name};{name};;;\n"
                        f"FN:{name}\n"
                        f"TEL;TYPE=CELL:{number}\n"
                        "END:VCARD\n\n"
                    )

            # Parse csv file
            elif self.input_file.endswith(".csv"):
                reader = csv.reader(f)
                contact_data = list(reader)
                
                for i, contact in enumerate(contact_data):
                    # When there is nothing in the "Phone" field of the contact record, the contact will not be created
                    if i != 0 and contact[0] == "":
                        continue
                    
                    sanitized_number, name, organization, title, email, address = self.sanitizeNumber(contact[0]), contact[1], contact[2], contact[3], contact[4], contact[5]
                    if not name:
                        name = f"Contact {i:03d}"
                    try: 
                        first, last = name.split()
                    except ValueError: 
                        first, last = name, ""
                    
                    out.write(
                        "BEGIN:VCARD\n"
                        "VERSION:3.0\n"
                        f"FN:{first} {last}\n"
                        f"N:{last};{first}\n"
                        f"ORG:{organization}\n"
                        f"TITLE:{title}\n"
                        f"TEL;TYPE=CELL:{sanitized_number}\n"
                        f"EMAIL:{email}\n"
                        f"ADR:{address}\n"
                        "END:VCARD\n\n"
                    )