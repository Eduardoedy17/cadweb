from datetime import datetime

def data_atual(request):
    """
    Retorna a data atual para ser usada nos templates (Slide 198)
    """
    return {
        'data_atual': datetime.now()
    }