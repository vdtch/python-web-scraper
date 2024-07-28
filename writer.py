import csv


def write_quote_to_csv_file(quotes: dict):
    # Read csv file and create if not exist
    csv_file = open('output/quotes.csv', 'w', encoding='utf-8', newline='')

    # Initialize writer object
    writer = csv.writer(csv_file)

    # Write the header of the file
    writer.writerow(['Text', 'Author', 'Tags'])

    # Write quotes in csv file
    for quote in quotes:
        writer.writerow(quote.values())
    
    csv_file.close()