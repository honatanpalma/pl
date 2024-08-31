# Disclaimer
This project is developed exclusively for educational and learning purposes. It is not intended for commercial use or any other unauthorized application.

# Prensa Libre Web Scraper and PDF Generator

This Python script automates the process of web scraping Prensa Libre newspaper images, converting them into a PDF, and sending the PDF via email.

## Features

* **Web Scraping:** Utilizes the `requests` library to efficiently retrieve images from the Prensa Libre website.
* **Image Processing:** Employs `img2pdf` to seamlessly combine the scraped images into a well-structured PDF document.
* **Date/Time Handling:** Leverages `datetime` and `pytz` to ensure accurate date and time management for image retrieval and PDF naming.
* **Email Automation:** Integrates with `smtplib` and `email` to automatically send the generated PDF via email.

## Prerequisites

* Python 3.x
* Required libraries (see `requirements.txt`)

## Installation

1. Clone the repository: `git clone https://github.com/honatanpalma/pl.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure token and email settings in the script.

## Usage

Run the script: `python web-scrapping-pl.py`

## How it Works

1. **Image Retrieval:** The script systematically sends HTTP requests to the Prensa Libre website using `requests`, targeting specific image URLs based on the current date.
2. **Image Processing:** Retrieved images are stored in memory, and `img2pdf` is employed to convert them into a PDF file.
3. **PDF Generation:** The PDF file is named using the current date and saved locally.
4. **Email Delivery:** The generated PDF is attached to an email and sent to the configured recipient using `smtplib` and `email`.

## Contributing

Contributions are welcome!

## Contact

For questions or feedback, please contact Honatan Palma at hapalmac@gmail.com
