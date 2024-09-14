import os
import subprocess
import uuid

def create_openssl_cnf(folder, country, state, city, organization, common_name):
    config_content = f"""
[ req ]
default_bits       = 2048
distinguished_name = req_distinguished_name
x509_extensions    = v3_req
prompt             = no

[ req_distinguished_name ]
C  = {country}
ST = {state}
L  = {city}
O  = {organization}
CN = {common_name}

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
    
    subprocess.run([
        'openssl', 'req', '-new', '-newkey', 'rsa:2048', '-days', '3650', '-nodes',
        '-x509', '-keyout', 'mycert.key', '-out', 'mycert.crt', '-config', 'openssl.cnf'
    ], check=True)
    
    subprocess.run([
        'openssl', 'pkcs12', '-export', '-out', 'mycert.pfx', '-inkey', 'mycert.key',
        '-in', 'mycert.crt', '-password', f'pass:{password}'
    ], check=True)
    
    print("Certificates created: mycert.key, mycert.crt, mycert.pfx")

def convert_to_der(folder):
    os.chdir(folder)
    
    subprocess.run([
        'openssl', 'x509', '-in', 'mycert.crt', '-outform', 'DER', '-out', 'mycert.der'
    ], check=True)
    
    print("DER format certificate created: mycert.der")

def sign_efi_files(folder, password, efi_bootloader_path):
    pfx_path = os.path.join(folder, 'mycert.pfx')
    
    subprocess.run([
        'signtool', 'sign', '/fd', 'sha256', '/f', pfx_path, '/p', password,
        '/tr', 'http://timestamp.digicert.com', '/td', 'sha256', efi_bootloader_path
    ], check=True)
    
    print(f"Signed the EFI bootloader: {efi_bootloader_path}")

def generate_guid():
    new_guid = uuid.uuid4()
    print(f"Generated GUID: {new_guid}")
    return new_guid

def main():
    password = input("Enter a password for the .pfx file: ")
    folder = input("Enter the folder where you want to save files: ")
    country = input("Enter Country (C): ")
    state = input("Enter State (ST): ")
    city = input("Enter City (L): ")
    organization = input("Enter Organization (O): ")
    common_name = input("Enter Common Name (CN): ")
    efi_bootloader_path = os.path.join(folder, 'loader.efi')
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    create_openssl_cnf(folder, country, state, city, organization, common_name)
    generate_certificates(folder, password)
    convert_to_der(folder)
    sign_efi_files(folder, password, efi_bootloader_path)
    generate_guid()

if __name__ == "__main__":
    main()
