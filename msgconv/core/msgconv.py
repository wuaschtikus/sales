import os
import extract_msg
from django.conf import settings
from asn1crypto import cms, pem
from email.message import EmailMessage
from email import policy
from email.parser import BytesParser
from mimetypes import guess_type

from sales.common_code import generate_file_hash

def msg_convert_msg_to_eml_with_signed(msg_file_path, eml_file_path, msg_attachments_path, additional_attachments=None):
    """
    Converts a .msg email file to an .eml file format and adds additional attachments if provided.

    Args:
        msg_file_path (str): The path to the .msg email file that needs to be converted.
        eml_file_path (str): The path where the resulting .eml file will be saved.
        additional_attachments (list, optional): List of file paths for additional attachments to add.

    Returns:
        str: The file path of the saved .eml file.
    """
    # Load the .msg file
    msg = extract_msg.Message(msg_file_path)
    
    # Create an EmailMessage object
    email_message = EmailMessage()
    
    # Set the subject, from, to, date
    email_message['Subject'] = msg.subject
    email_message['From'] = msg.sender
    email_message['Date'] = msg.date
    email_message['To'] = msg.recipients 

    # Set the body of the email
    if msg.body is not None:
        email_message.set_content(msg.body)
    
    # Handle additional attachments from files
    if additional_attachments:
        for file_path in additional_attachments:
            path = os.path.join(msg_attachments_path, os.path.basename(file_path))
            if os.path.isfile(path):
                
                with open(path, 'rb') as attachment_file:
                    file_data = attachment_file.read()
                    file_name = os.path.basename(path)
                    maintype, subtype = guess_type(file_name)[0].split('/') if guess_type(file_name)[0] else ('application', 'octet-stream')
                    
                    email_message.add_attachment(
                        file_data,
                        maintype=maintype,
                        subtype=subtype,
                        filename=file_name
                    )
    
    # Save the email message as an .eml file
    with open(eml_file_path, 'wb') as eml_file:
        eml_file.write(email_message.as_bytes())
    
    return eml_file_path

def msg_extract_info(msg_file_path):
    """
    Extracts various pieces of information from a .msg email file.

    Args:
        msg_file_path (str): The path to the .msg email file.

    Returns:
        dict: A dictionary containing the following extracted information:
            - "message_date" (str): The date the message was created, formatted as "Month Day, Year HH:MM AM/PM".
            - "received_by_server_date" (str): The date the message was received by the server, formatted as "Month Day, Year HH:MM AM/PM".
            - "email_addresses" (list of str): A list of email addresses, including the recipients and the sender.
            - "attachment_count" (int): The number of attachments in the email.
            - "subject" (str): The subject of the email.
            - "is_sent" (bool): Whether the email was marked as sent.
    """
    # Load the .msg file
    msg = extract_msg.Message(msg_file_path)
    
    # Extract message date
    msg_date = msg.date
    readable_msg_date = msg_date.strftime("%B %d, %Y %I:%M %p")
    
    # Extract received by server date
    received_by_server_date = msg.receivedTime
    readable_received_by_server_date = received_by_server_date.strftime("%B %d, %Y %I:%M %p")
    
    # Extract email addresses
    email_addresses = []
    for rec in msg.recipients:
        email_addresses.append(rec.email)
    email_addresses.append(msg.sender)

    # Extract subject
    subject = msg.subject

    # Check if the email was marked as sent
    is_sent = msg.isSent

    # Return all extracted information in a dictionary
    return {
        "message_date": readable_msg_date,
        "received_by_server_date": readable_received_by_server_date,
        "email_addresses": email_addresses,
        "subject": subject,
        "is_sent": is_sent, 
        'msg_hash': generate_file_hash(msg_file_path),
    }

def msg_extract_attachments(msg_file_path, output_dir, download_base_url):
    """
    Extracts attachments from a .msg file and stores them in the specified output directory.

    Args:
        msg_file_path (str): The path to the .msg file.
        output_dir (str): The directory where attachments should be saved.
        download_base_url (str): The base URL for downloading the attachments.

    Returns:
        list: A list of dictionaries, each containing the filename and download path.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load the .msg file
    msg = extract_msg.Message(msg_file_path)
    # List to store dictionaries with filename and download path
    attachments_info = []
    
    # Loop through the attachments in the .msg file
    for attachment in msg.attachments:
        # Get the attachment file name
        attachment_filename = attachment.longFilename if attachment.longFilename else attachment.shortFilename
        attachment_filepath = os.path.join(output_dir, attachment_filename)

        if attachment.mimetype == 'multipart/signed':
            attachments_info = msg_extract_signed_attachments(attachment.data, output_dir, download_base_url)
        else:
            # Write the attachment to disk
            with open(attachment_filepath, 'wb') as f:
                f.write(attachment.data)
            
            # Construct the download URL for the attachment
            download_url = os.path.join(download_base_url, attachment_filename)
            
            # Add a dictionary with filename and download path to the list
            attachments_info.append({
                'filename': attachment_filename,
                'download_path': download_url,
                'signed_attachment': False
            })

    return attachments_info

def msg_extract_signed_attachments(email_bytes, output_dir, download_base_url):
    """
    Parses an email provided as bytes, extracting and saving all attachments, and returns attachment info.

    Args:
        email_bytes (bytes): The email content in bytes.
        output_dir (str): The directory where attachments should be saved.
        download_base_url (str): The base URL for downloading the attachments.

    Returns:
        list: A list of dictionaries, each containing the filename and download path.
    """
    attachments_info = []
    
    # Ensure email_bytes is in bytes format
    if isinstance(email_bytes, str):
        email_bytes = email_bytes.encode('utf-8')

    # Parse the email from bytes
    msg = BytesParser(policy=policy.default).parsebytes(email_bytes)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process the entire message, starting with the top-level part
    process_part(msg, output_dir, download_base_url, attachments_info)

    return attachments_info

def process_part(part, output_dir, download_base_url, attachments_info):
    """
    Processes a single MIME part, extracting and saving attachments.

    Args:
        part (email.message.EmailMessage): A single part of the email message.
        output_dir (str): The directory where attachments should be saved.
        download_base_url (str): The base URL for downloading the attachments.
        attachments_info (list): A list to accumulate attachment information.
    """
    content_type = part.get_content_type()
    content_disposition = part.get("Content-Disposition", None)
    filename = part.get_filename()
    
    # If the part is multipart, recursively process each sub-part
    if part.is_multipart():
        for subpart in part.iter_parts():
            process_part(subpart, output_dir, download_base_url, attachments_info)
    # Handle attachments (files or images)
    elif content_disposition and filename:
        attachment_path = os.path.join(output_dir, filename)
        with open(attachment_path, "wb") as file:
            file.write(part.get_payload(decode=True))
        # Construct the download URL for the attachment
        download_url = os.path.join(download_base_url, filename)
        attachments_info.append({
            'filename': filename,
            'download_path': download_url,
            'signed_attachment': True
        })

    return attachments_info

def read_p7s(file_path):
    """
    Reads and parses a .p7s file (PKCS7 signature file) to extract and return the signer issuer information.

    Args:
        file_path (str): The path to the .p7s file.

    Returns:
        str: A formatted string with the signer issuer's human-friendly information.

    Raises:
        ValueError: If the file is not a valid PKCS7 file or if parsing fails.
    """
    # Read the .p7s file in binary mode
    with open(file_path, 'rb') as f:
        p7s_data = f.read()

    # Check if the file is in PEM format and convert it to DER format if needed
    if pem.detect(p7s_data):
        _, _, p7s_data = pem.unarmor(p7s_data)

    # Load the PKCS7 content
    content_info = cms.ContentInfo.load(p7s_data)
    signed_data = content_info['content']

    # Iterate over signer information and return the issuer details
    for signer_info in signed_data['signer_infos']:
        sid = signer_info['sid']
        issuer_and_serial = sid.chosen
        return f"Signer Issuer: {issuer_and_serial['issuer'].human_friendly}"

    return None  # If no signer information is found, return None