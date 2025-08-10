from celery import shared_task
from .models import FileUpload
import docx

@shared_task
def process_file_word_count(file_id):
    try:
        file_record = FileUpload.objects.get(id=file_id)
        file_path = file_record.file.path
        print(file_path)
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                print(text)
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            file_record.status = 'failed'
            file_record.save()
            return

        word_count = len(text.split())
        file_record.word_count = word_count
        file_record.status = 'completed'
        file_record.save()

    except Exception as e:
        file_record.status = 'failed'
        file_record.save()
