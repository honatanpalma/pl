# Import necessary libraries for subprocess management, web requests, image-to-PDF conversion, date/time handling, and email functionality
import subprocess
import requests
import img2pdf
import datetime
import pytz
import smtplib
from email.message import EmailMessage

# Define a list of required Python libraries
libraries = ["requests", "img2pdf", "datetime", "pytz"]

# Iterate through the list and install each library using pip
for library in libraries:
    # Execute the pip install command for the current library, capturing output
    result = subprocess.run(["pip", "install", library], capture_output=True)

    # Check if there was an error during the installation
    if result.returncode != 0:
        # Display an error message with the library name and the error details
        print(f"Error occurred while installing library {library}:")
        print(result.stderr.decode())
    else:
        # Display a success message indicating the library was installed
        print(f"Library {library} installed successfully.")

# Set the timezone to Guatemala
tz = pytz.timezone('America/Guatemala')

# Get the current timestamp in the specified timezone
now = datetime.datetime.now(tz)

# Format the current date as YYYYMMDD
formatted_date = now.strftime("%Y%m%d")

# Format the current date for email subject
email_date = now.strftime("%m/%d/%Y")

# Base URL for image retrieval, incorporating the formatted date
base_url = "https://foservices.prensalibre.com/viewer/get_protected_source?protected={}%2Fnormal%2FPL_{}_001_".format(formatted_date, formatted_date)

# Define the range of image numbers to process
image_numbers = range(1, 80)

# Flag to indicate if an image was found
image_found = True

# List to store image data
image_list = []

# Iterate through image numbers, attempting to retrieve each image
for image_number in image_numbers:
    # Check if the previous image was found
    if image_found:
        # Format the image number with leading zeros and add the .jpg extension
        image_filename = f"{image_number:02d}.jpg"

        # Construct the complete image URL
        image_url = base_url + image_filename + "&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2lkLnBpYW5vLmlvIiwic3ViIjoiMzM0NjY5IiwiYXVkIjoiTldyU1FhUWpGZCIsImxvZ2luX3RpbWVzdGFtcCI6IjE3MjQxNjMwNjcxMjEiLCJnaXZlbl9uYW1lIjoiSG9uYXRhbiIsImZhbWlseV9uYW1lIjoiUGFsbWEiLCJlbWFpbCI6ImhhcGFsbWFjQGdtYWlsLmNvbSIsImVtYWlsX2NvbmZpcm1hdGlvbl9yZXF1aXJlZCI6ZmFsc2UsImV4cCI6MTcyNjc5MTA2NywiaWF0IjoxNzI0MTYzMDY3LCJqdGkiOiJUSTBzQUw3SDBRc2lpc3FqIiwicGFzc3dvcmRUeXBlIjoicGFzc3dvcmQiLCJyIjp0cnVlLCJscyI6IklEIiwiZmlyc3ROYW1lIjoiSG9uYXRhbiIsImxhc3ROYW1lIjoiUGFsbWEiLCJ2YWxpZCI6dHJ1ZSwidWlkIjoiMzM0NjY5IiwiY29uZmlybWVkIjp0cnVlLCJrZXlQbCI6IlNwZFRtaGtuUkR0UDJiR2djbzh4In0.DW7KB9eT5-6ZvSN686XoeLKLYTO4S48_FCN-Xi8OyPM"

        # Send a GET request to retrieve the image
        response = requests.get(image_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Retrieve the image content as bytes
            image_bytes = response.content

            # Add the image bytes to the list
            image_list.append(image_bytes)

            # Display a success message indicating the image was retrieved
            print(f"Image {image_filename} retrieved successfully.")
        else:
            # Display an error message with the image filename and the status code
            print(f"Failed to retrieve image {image_filename}. Status code: {response.status_code}")

            # Set the image_found flag to False to stop further attempts
            image_found = False
    else:
        # Break the loop if a previous image retrieval failed
        break

# Check if any images were retrieved
if image_list:
    # Define the output PDF filename using the formatted date
    pdf_filename = f"PL_{formatted_date}.pdf"

    # Ensure the PDF filename doesn't conflict with any image filenames
    if pdf_filename not in [f"{n:02d}.pdf" for n in image_numbers]:
        # Validate the PDF filename for invalid characters and spaces
        if not any(c in pdf_filename for c in "?*:<>\n|\"/") and " " not in pdf_filename:
            # Create the PDF file from the collected image data
            with open(pdf_filename, "wb") as f:
                f.write(img2pdf.convert(image_list))

            # Display a success message indicating the PDF creation
            print(f"PDF file {pdf_filename} created successfully.")

            # Create an email message
            msg = EmailMessage()
            msg["Subject"] = f"Prensa Libre for {email_date}"
            msg["From"] = "noreply@gmail.com"
            msg["Bcc"] = ["hapalmac@gmail.com"]

            # Set the email body
            msg.set_content(
                f"Hello,\n\nPlease find attached today's Prensa Libre.\n\nBest regards."
            )

            # Attach the PDF file to the email
            with open(pdf_filename, "rb") as f:
                msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_filename)

            # Send the email using Gmail's SMTP server
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login("hapalmac@gmail.com", "dpsxnrpaovvkunew")  # Replace with your Gmail credentials
                server.send_message(msg)

                # Display a success message indicating the email was sent
                print(f"Email with attached {pdf_filename} sent successfully.")
        else:
            # Display an error message if the PDF filename is invalid
            print("The PDF filename contains invalid characters. Please modify the filename.")
    else:
        # Display an error message if the PDF filename conflicts with an image filename
        print("The PDF filename conflicts with an image filename. Please change the PDF filename.")
else:
    # Display an error message if no images were retrieved
    print("No images were retrieved. Please verify the URL and token.")
