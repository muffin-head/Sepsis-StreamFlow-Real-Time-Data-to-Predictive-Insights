import fastavro
def read_avro_file(file_path):
    """
    Reads and prints the contents of an Avro file.
    :param file_path: Path to the Avro file.
    """
    with open(file_path, 'rb') as file:
        reader = fastavro.reader(file)
        for record in reader:
            print(record)

# Example usage
file_path = "09.avro"
read_avro_file(file_path)
