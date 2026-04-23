import sys

def strip_non_ascii(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Keep only ASCII characters (0-127)
        clean_content = "".join(i for i in content if ord(i) < 128)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clean_content)
        print(f"Successfully stripped non-ASCII from {filepath}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    strip_non_ascii(r"c:\Users\jhnap\OneDrive\Desktop\HackXtreme_main\GlobalSentry-Web\api.py")

