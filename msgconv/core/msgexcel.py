import extract_msg
import pandas as pd
import os
import email
from email import policy
from email.parser import BytesParser

def extract_msg_info(msg_file):
    """
    Extracts relevant information from a .msg file.

    Parameters:
    msg_file (str): The file path of the .msg file to be processed.

    Returns:
    dict: A dictionary containing the extracted information with the following keys:
        - 'Filename' (str): The name of the .msg file.
        - 'Subject' (str): The subject of the email.
        - 'Sender' (str): The sender's email address.
        - 'To' (str): The recipients' email addresses.
        - 'Date' (str): The date the email was sent.
        - 'Body' (str): The body content of the email.
        - 'Attachments' (str): A comma-separated list of attachment filenames, or 'None' if there are no attachments.
    """
    msg = extract_msg.Message(msg_file)
    
    data = {
        'Filename': os.path.basename(msg_file),
        'Subject': msg.subject,
        'Sender': msg.sender,
        'To': msg.to,
        'Date': msg.date,
        'Body': msg.body,
        'Attachments': ', '.join([att.filename for att in msg.attachments]) if msg.attachments else 'None'
    }
    
    return data

def extract_eml_info(eml_file):
    """
    Extracts relevant information from a .eml file.

    Parameters:
    eml_file (str): The file path of the .eml file to be processed.

    Returns:
    dict: A dictionary containing the extracted information with the following keys:
        - 'Filename' (str): The name of the .eml file.
        - 'Subject' (str): The subject of the email.
        - 'Sender' (str): The sender's email address.
        - 'To' (str): The recipients' email addresses.
        - 'Date' (str): The date the email was sent.
        - 'Body' (str): The body content of the email.
        - 'Attachments' (str): A comma-separated list of attachment filenames, or 'None' if there are no attachments.
    """
    with open(eml_file, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    data = {
        'Filename': os.path.basename(eml_file),
        'Subject': msg['subject'],
        'Sender': msg['from'],
        'To': msg['to'],
        'Date': msg['date'],
        'Body': msg.get_body(preferencelist=('plain')).get_content() if msg.is_multipart() else msg.get_payload(),
        'Attachments': ', '.join(part.get_filename() for part in msg.iter_attachments()) if msg.iter_attachments() else 'None'
    }
    
    return data

def convert_multiple_msgs_and_emls_to_excel(files, output_excel_file):
    """
    Processes multiple .msg and .eml files, extracts their information, and saves the data to a single Excel file.

    Parameters:
    files (list of str): A list of file paths to .msg and .eml files to be processed.
    output_excel_file (str): The file path where the resulting Excel file will be saved.

    Returns:
    None
    """
    all_data = []
    
    for file in files:
        if file.endswith('.msg'):
            data = extract_msg_info(file)
        elif file.endswith('.eml'):
            data = extract_eml_info(file)
        all_data.append(data)
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(all_data)
    
    # Write the DataFrame to an Excel file
    df.to_excel(output_excel_file, index=False)

