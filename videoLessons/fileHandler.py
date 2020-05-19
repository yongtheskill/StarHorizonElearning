from django.core.files.storage import default_storage

#to get video URL
from django.conf import settings


def handle_uploaded_file(f, videoID):
    fileName = "%s.mp4" % (videoID) 
    """
    if not default_storage.exists(fileName):
        with default_storage.open(fileName, 'w') as destinationFile:
            for chunk in f.chunks():
                destinationFile.write(chunk)
        return "https://%s/%s/%s" % (settings.AWS_S3_CUSTOM_DOMAIN, default_storage.location, fileName)
    else:
        return "error"
    """
        
    return "https://%s/%s/%s" % (settings.AWS_S3_CUSTOM_DOMAIN, default_storage.location, fileName)
