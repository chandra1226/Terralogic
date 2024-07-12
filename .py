from google.cloud import documentai_v1 as documentai
from google.cloud import storage

def bulk_process_documents(project_id, location, processor_id, folder_path):
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)

    # Get a list of files in the folder
    files = os.listdir(folder_path)

    # Process each file
    for file in files:
        file_path = os.path.join(folder_path, file)
        mime_type = 'application/pdf'  # or 'image/jpeg' for JPG files

        # Read the file into memory
        with open(file_path, "rb") as image:
            image_content = image.read()

        # Load GCS file to Document AI
        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

        # Configure the process request
        request = documentai.ProcessRequest(name=name, raw_document=raw_document)

        # Process the document
        result = client.process_document(request)

        # Extract the extracted data
        document = result.document
        text = ''
        for page in document.pages:
            for form_field in page.form_fields:
                text += f"Field: {form_field.field_name}, Value: {form_field.value}\n"
        print(text)

# Example usage
project_id = 'your-project-id'
location = 'us'
processor_id = 'your-processor-id'
folder_path = 'path/to/your/documents/folder'

bulk_process_documents(project_id, location, processor_id, folder_path)
