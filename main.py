import argparse
import sys
from pathlib import Path
from VCFGenerator import VCFGenerator

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Convert a TXT file of phone numbers into a VCF contact file"
    )
    parser.add_argument(
        "-i", "--input",
        help="Path to input .txt file containing phone numbers"
    )
    parser.add_argument(
        "-o", "--output",
        default="",
        help="Output .vcf file (default: contacts.vcf)"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    VCFG = VCFGenerator(args.input, args.output)
    VCFG.generateVCF() 


if __name__ == "__main__":
    main()
