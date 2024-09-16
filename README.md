Prompts for User Input: Asks for the password, folder location, and certificate details (country, state, city, organization, and common name).
Creates OpenSSL Configuration: Generates openssl.cnf with user-provided details.
Generates Certificates: Creates .key, .crt, and .pfx files using OpenSSL.
Converts Certificate: Converts .crt to .der format.
Signs EFI Bootloader: Signs the file using the generated .pfx file.
Generates GUID: Outputs a new GUID.
