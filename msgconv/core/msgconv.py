import os
import extract_msg
from email.message import EmailMessage

def msg_convert_msg_to_eml(msg_file_path, eml_file_path):
    """
    Converts a .msg email file to an .eml file format.

    Args:
        msg_file_path (str): The path to the .msg email file that needs to be converted.
        eml_file_path (str): The path where the resulting .eml file will be saved.

    Returns:
        str: The file path of the saved .eml file.

    Description:
        This function loads a .msg email file and converts it into an .eml file format. It transfers
        the subject, sender, recipients, date, and body from the .msg file to an EmailMessage object.
        It also handles any attachments, adding them to the EmailMessage object. The function then
        writes the EmailMessage object to the specified .eml file path.

    Example:
        msg_file = '/path/to/email.msg'
        eml_file = '/path/to/output/email.eml'
        converted_file_path = msg_convert_msg_to_eml(msg_file, eml_file)
        print(f"EML file saved at: {converted_file_path}")

    Notes:
        - The function assumes the .msg file is properly formatted and that all necessary attributes
          (like subject, sender, recipients, etc.) are present.
        - Attachments are added to the .eml file as octet-streams with their original filenames.
    """
    # Load the .msg file
    msg = extract_msg.Message(msg_file_path)
    
    # Create an EmailMessage object
    email_message = EmailMessage()
    
    # Set the subject, from, to, date
    email_message['Subject'] = msg.subject
    email_message['From'] = msg.sender
    email_message['To'] = msg.recipients
    email_message['Date'] = msg.date
    
    # Set the body of the email
    if msg.body is not None:
        email_message.set_content(msg.body)
    
    # Handle attachments
    for attachment in msg.attachments:
        email_message.add_attachment(
            attachment.data,
            maintype='application',
            subtype='octet-stream',
            filename=attachment.longFilename
        )
        print('Added attachment' + attachment.longFilename)
    
    # Save the email message as an .eml file
    with open(eml_file_path, 'wb') as eml_file:
        eml_file.write(email_message.as_bytes())
    
    print(f"Converted {msg_file_path} to {eml_file_path}")
    
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
    
    # Count attachments
    count_attachments = len(msg.attachments) if msg.attachments else 0

    # Extract subject
    subject = msg.subject

    # Check if the email was marked as sent
    is_sent = msg.isSent

    # Return all extracted information in a dictionary
    return {
        "message_date": readable_msg_date,
        "received_by_server_date": readable_received_by_server_date,
        "email_addresses": email_addresses,
        "attachment_count": count_attachments,
        "subject": subject,
        "is_sent": is_sent
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
        
        # Write the attachment to disk
        with open(attachment_filepath, 'wb') as f:
            f.write(attachment.data)
        
        # Construct the download URL for the attachment
        download_url = os.path.join(download_base_url, attachment_filename)
        
        # Add a dictionary with filename and download path to the list
        attachments_info.append({
            'filename': attachment_filename,
            'download_path': download_url
        })

    return attachments_info
