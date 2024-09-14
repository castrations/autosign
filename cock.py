import os
import subprocess
import uuid

def create_openssl_cnf(folder):
    config_content = """
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
x509_extensions    = v3_req
prompt             = no

[ req_distinguished_name ]
C  = UK
ST = London
L  = London
O  = Linus Media Group
CN = Linus

[ v3_req ]
keyUsage = critical, digitalSignature
extendedKeyUsage = codeSigning
basicConstraints = critical, CA:FALSE
    """
    
    config_path = os.path.join(folder, 'openssl.cnf')
    with open(config_path, 'w') as file:
        file.write(config_content)
    print(f"openssl.cnf file created at {config_path}")
    return config_path

def generate_certificates(folder, password):
    os.chdir(folder)
    
    # key etc
    subprocess.run([
        'openssl', 'req', '-new', '-newkey', 'rsa:2048', '-days', '3650', '-nodes',
        '-x509', '-keyout', 'mycert.key', '-out', 'mycert.crt', '-config', 'openssl.cnf'
    ], check=True)
    
    # ignore
    subprocess.run([
        'openssl', 'pkcs12', '-export', '-out', 'mycert.pfx', '-inkey', 'mycert.key',
        '-in', 'mycert.crt', '-password', f'pass:{password}'
    ], check=True)
    
    print("Certificates created: mycert.key, mycert.crt, mycert.pfx")

# der for bios
def convert_to_der(folder):
    os.chdir(folder)
    
    # Convert to DER format
    subprocess.run([
        'openssl', 'x509', '-in', 'mycert.crt', '-outform', 'DER', '-out', 'mycert.der'
    ], check=True)
    
    print("DER format certificate created: mycert.der")

# Step 4: Sign
def sign_efi_files(folder, password, efi_bootloader_path):
    # Path to the .pfx file
    pfx_path = os.path.join(folder, 'mycert.pfx')
    
    # Sign the EFI or whatever it is
    subprocess.run([
        'signtool', 'sign', '/fd', 'sha256', '/f', pfx_path, '/p', password,
        '/tr', 'http://timestamp.digicert.com', '/td', 'sha256', efi_bootloader_path
    ], check=True)
    
    print(f"Signed the EFI bootloader: {efi_bootloader_path}")

# GUID
def generate_guid():
    new_guid = uuid.uuid4()
    print(f"Generated GUID: {new_guid}")
    return new_guid

# Main function
def main():
    # Hardcoded values
    password = 'Linus'
    folder = r'C:\Users\brandon\Desktop\zk'
    efi_bootloader_path = os.path.join(folder, 'loader.efi')  # Hardcoded path to loader.efi

    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Step 1: Create openssl.cnf
    create_openssl_cnf(folder)
    
    # Step 2: Generate certificates
    generate_certificates(folder, password)
    
    # Step 3: Convert to DER format
    convert_to_der(folder)
    
    # Step 4: Sign EFI 
    sign_efi_files(folder, password, efi_bootloader_path)
    
    # Step 5: Generate a GUID for later use
    generate_guid()

if __name__ == "__main__":
    main()
