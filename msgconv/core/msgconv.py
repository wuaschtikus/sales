
import extract_msg
from email.message import EmailMessage

def convert_msg_to_eml(msg_file_path, eml_file_path):
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

# Example usage:
# msg_file = "../data/msg/Test1.msg"
# eml_file = "../data/eml/Test1.eml"
# convert_msg_to_eml(msg_file, eml_file)
