try:
    from google.cloud import translate
except:
    exit("Please run \"pip install --upgrade google-cloud-translate\"")


def translate_text(target, text):
    return translate.Client().translate(text, target_language=target)
