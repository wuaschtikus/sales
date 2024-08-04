import os
import extract_msg
from email.message import EmailMessage

def msg_convert_msg_to_eml(msg_file_path, eml_file_path):
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

def msg_count_attachments(msg_file_path):
    if extract_msg.Message(msg_file_path).attachments:
        count_attachments = len(extract_msg.Message(msg_file_path).attachments)
        return count_attachments
    
    return 0

def msg_date(msg_file_path):
    msg = extract_msg.Message(msg_file_path)
    
    return msg.contacts

def msg_email_addresses(msg_file_path):
    msg = extract_msg.Message(msg_file_path)
    addresses = []
    for rec in msg.recipients:
        addresses.append(rec.email)
    addresses.append(msg.sender)
    
    return addresses
    
