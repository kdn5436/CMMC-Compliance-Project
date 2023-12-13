import pyautogui
import time
import pyperclip
import yaml
import os
from classifystig import win10_task_relevant_info
def main():
    with open("../stiglevel2/roles/Win10STIG/tasks/cat2.yml", 'rb') as f:
        content = f.read()

        # Decode the content, replacing any offending characters
        content_decoded = content.decode('utf-8', errors='replace')
    
        # Now load the cleaned content with the YAML parser
        tasks = yaml.load(content_decoded, Loader=yaml.FullLoader)

        for task in tasks:
            id, name, typ, impl = win10_task_relevant_info(task)
            input_str = f"""You are a component in a program that maps an ansible security implementation to a relevant security control in compliance with the CMMC Model V2 Security controls.
You will be given an ansible task that implements a security control, and you will be respond with only the Title of the security control that best represents the ansible task.
Below is a list of CMMC Model V2 Level 2 Security Controls. Controls are grouped into groups based on the type of security control they are. Each control has a Title and a Description.
Controls:
```
Group: ACCESS CONTROL (AC)
- Title: Authorized Access Control
- - Description: Limit information system access to authorized users, processes acting on behalf of authorized users, or devices (including other information systems).

- Title: Transaction & Function Control
- - Description: Limit information system access to the types of transactions and functions that authorized users are permitted to execute. 

- Title: External Connections
- - Description: Verify and control/limit connections to and use of external information systems. 

- Title: Control Public Information
- - Description: Control information posted or processed on publicly accessible information systems.

- Title: Separation of Duties
- - Description: Separate the duties of individuals to reduce the risk of malevolent activity without collusion.

- Title: Least Privilege
- - Description: Employ the principle of least privilege, including for specific security functions and privileged accounts.

- Title: Non-Privileged Account Use
- - Description: Use non-privileged accounts or roles when accessing nonsecurity functions.

- Title: Privileged Functions
- - Description: Prevent non-privileged users from executing privileged functions and capture the execution of such functions in audit logs.

- Title: Unsuccessful Logon Attempts
- - Description: Limit unsuccessful logon attempts. 

- Title: Privacy & Security Notices
- - Description: Provide privacy and security notices consistent with applicable CUI rules.

- Title: Session Lock
- - Description: Use session lock with pattern-hiding displays to prevent access and viewing of data after a period of inactivity. 

- Title: Session Termination
- - Description: Terminate (automatically) a user session after a defined condition.

- Title: Control Remote Access
- - Description: Monitor and control remote access sessions.

- Title: Remote Access Confidentiality
- - Description: Employ cryptographic mechanisms to protect the confidentiality of remote access sessions.

- Title: Remote Access Routing
- - Description: Route remote access via managed access control points. 

- Title: Privileged Remote Access
- - Description: Authorize remote execution of privileged commands and remote access to security-relevant information. 

Group: AUDIT AND ACCOUNTABILITY (AU)
- Title: System Auditing
- - Description: Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity. 

- Title: User Accountability
- - Description: Ensure that the actions of individual system users can be uniquely traced to those users, so they can be held accountable for their actions.

- Title: Event Review
- - Description: Review and update logged events.

- Title: Audit Failure Alerting
- - Description: Alert in the event of an audit logging process failure. 

- Title: Audit Correlation
- - Description: Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity.

- Title: Reduction & Reporting
- - Description: Provide audit record reduction and report generation to support on-demand analysis and reporting.

- Title: Authoritative Time Source
- - Description: Provide a system capability that compares and synchronizes internal system clocks with an authoritative source to generate time stamps for audit records.

- Title: Audit Protection
- - Description: Protect audit information,%ßand audit logging tools from unauthorized access, modification, and deletion.

- Title: Audit Management
- - Description: Limit management of audit logging functionality to a subset of privileged users.,%ß

Group: CONFIGURATION MANAGEMENT (CM)
- Title: Security Configuration Enforcement
- - Description: Establish and enforce security configuration settings for information technology products employed in organizational systems.

- Title: System Change Management
- - Description: Track, review, approve or disapprove, and log changes to organizational systems. 

- Title: Least Functionality
- - Description: Employ the principle of least functionality by configuring organizational systems to provide only essential capabilities. 

- Title: Nonessential Functionality
- - Description: Restrict, disable, or prevent the use of nonessential programs, functions, ports, protocols, and services. 

- Title: Application Execution Policy
- - Description: Apply deny-by-exception (blacklisting) policy to prevent the use of unauthorized software or deny-all, permit-by-exception (whitelisting) policy to allow the execution of authorized software. 

- Title: User-Installed Software
- - Description: Control and monitor user-installed software.

Group: IDENTIFICATION AND AUTHENTICATION (IA)
- Title: Identification
- - Description: Identify information system users, processes acting on behalf of users, or devices.

- Title: Authentication
- - Description: Authenticate (or verify) the identities of those users, processes, or devices, as a prerequisite to allowing access to organizational information systems.

- Title: Multifactor Authentication
- - Description: Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts. 

- Title: Replay-Resistant Authentication
- - Description: Employ replay-resistant authentication mechanisms for network access to privileged and non-privileged accounts.

- Title: Identifier Reuse
- - Description: Prevent reuse of identifiers for a defined period. 

- Title: Identifier Handling
- - Description: Disable identifiers after a defined period of inactivity. 

- Title: Password Complexity
- - Description: Enforce a minimum password complexity and change of characters when new passwords are created.

- Title: Password Reuse
- - Description: Prohibit password reuse for a specified number of generations.

- Title: Temporary Passwords
- - Description: Allow temporary password use for system logons with an immediate change to a permanent password. 

- Title: Cryptographically-Protected Passwords
- - Description: Store and transmit only cryptographically-protected passwords. 

- Title: Obscure Feedback
- - Description: Obscure feedback of authentication information. 

Group: MAINTENANCE (MA)
- Title: Nonlocal Maintenance
- - Description: Require multifactor authentication to establish nonlocal maintenance sessions via external network connections and terminate such connections when nonlocal maintenance is complete.

Group: MEDIA PROTECTION (MP)
- Title: Media Access
- - Description: Limit access to CUI on system media to authorized users.

- Title: Removable Media
- - Description: Control the use of removable media on system components.

- Title: Protect Backups
- - Description: Protect the confidentiality of backup CUI at storage locations. 

Group: PHYSICAL PROTECTION (PE)
- Title: Monitor Facility
- - Description: Protect and monitor the physical facility and support infrastructure for organizational systems.

- Title: Alternative Work Sites
- - Description: Enforce safeguarding measures for CUI at alternate work sites.

Group: SYSTEM AND COMMUNICATIONS PROTECTION (SC)
- Title: Boundary Protection
- - Description: Monitor, control, and protect organizational communications (i.e., information transmitted or received by organizational information systems) at the external boundaries and key internal boundaries of the information systems.

- Title: Public-Access System Separation
- - Description: Implement subnetworks for publicly accessible system components that are physically or logically separated from internal networks.

- Title: Security Engineering
- - Description: Employ architectural designs, software development techniques, and systems engineering principles that promote effective information security within organizational systems.

- Title: Role Separation
- - Description: Separate user functionality from system management functionality. 

- Title: Shared Resource Control
- - Description: Prevent unauthorized and unintended information transfer via shared system resources. 

- Title: Network Communication by Exception
- - Description: Deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception).

- Title: Split Tunneling
- - Description: Prevent remote devices from simultaneously establishing non-remote connections with organizational systems and communicating via some other connection to resources in external networks (i.e., split tunneling). 

- Title: Data in Transit
- - Description: Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission unless otherwise protected by alternative physical safeguards.

- Title: Connections Termination
- - Description: Terminate network connections associated with communications sessions at the end of the sessions or after a defined period of inactivity. 

- Title: Key Management
- - Description: Establish and manage cryptographic keys for cryptography employed in organizational systems. 

- Title: CUI Encryption
- - Description: Employ FIPS-validated cryptography when used to protect the confidentiality of CUI. 

- Title: Collaborative Device Control
- - Description: Prohibit remote activation of collaborative computing devices and provide indication of devices in use to users present at the device. 

- Title: Mobile Code
- - Description: Control and monitor the use of mobile code. 

- Title: Voice over Internet Protocol
- - Description: Control and monitor the use of Voice over Internet Protocol (VoIP) technologies.

- Title: Communications Authenticity
- - Description: Protect the authenticity of communications sessions.

- Title: Data at Rest
- - Description: Protect the confidentiality of CUI at rest.

Group: SYSTEM AND INFORMATION INTEGRITY (SI)
- Title: Flaw Remediation
- - Description: Identify, report, and correct information and information system flaws in a timely manner.

- Title: Malicious Code Protection
- - Description: Provide protection from malicious code at appropriate locations within organizational information systems.

- Title: Update Malicious Code Protection
- - Description: Update malicious code protection mechanisms when new releases are available.

- Title: System & File Scanning
- - Description: Perform periodic scans of the information system and real-time scans of files from external sources as files are downloaded, opened, or executed.

- Title: Security Alerts & Advisories
- - Description: Monitor system security alerts and advisories and take action in response.

- Title: Monitor Communications for Attacks
- - Description: Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.

- Title: Identify Unauthorized Use
- - Description: Identify unauthorized use of organizational systems. 
```

If the provided task is not relevant to any of the controls, respond with the word 'NONE'.
You must only output the title of the control that best represents the task, or 'NONE'.  For example, if the task is to "Ensure that the system is configured to audit System - Security State Change successes", you would respond with "System Auditing" because that is the title of the control that best represents the task.

task:
```
- name: {name}\n  {impl}
```"""
            pyperclip.copy(input_str)

            # get contents of the clipboard
            print(pyperclip.paste())

            pyautogui.moveTo(3185, 2052)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('tab')
            pyautogui.press('space')
            time.sleep(15)
            pyautogui.moveTo(3185, 1901)
            pyautogui.click()
            time.sleep(.01)
            pyautogui.click()
            time.sleep(.01)
            pyautogui.click()
            time.sleep(.01)
            pyautogui.hotkey('ctrl', 'c')
            # use the os library to append the contents of the clipboard to a file
            with open("classifications.txt", "a") as f:
                f.write(f"{name}\n{pyperclip.paste()}\n\n")
                f.close()
            # pyautogui.moveTo(800, 1901)
            # pyautogui.click()
            # pyautogui.hotkey('ctrl', 'v')
            # # pyautogui.press('enter')


if __name__ == "__main__":
    main()