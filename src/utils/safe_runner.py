# src/utils/safe_runner.py
import threading

def run_with_timeout(func, *args, timeout_s=5.0, **kwargs):
    """
    Executa uma função com timeout. Retorna dicionário com status:
    - 'ok': execução normal
    - 'timeout': ultrapassou tempo limite
    - 'error': ocorreu exceção
    """
    result_container = {"result": None, "status": None, "error": None}

    def target():
        try:
            result_container["result"] = func(*args, **kwargs)
            result_container["status"] = "ok"
        except Exception as e:
            result_container["status"] = "error"
            result_container["error"] = str(e)

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout_s)

    if thread.is_alive():
        result_container["status"] = "timeout"
        # thread continua viva mas será ignorada
        # não há forma segura de matar thread em Python nativo
        # normalmente substituímos a função por algo mais robusto se necessário

    return result_container
