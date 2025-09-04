import uvicorn
import os
from src.settings import settings



def init_required_folders():
    cache_path = '.temp'
    log_path = settings.LOG_FOLDER
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    if not os.path.exists(log_path):
        os.makedirs(log_path) 

def run():
    init_required_folders()
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload_excludes="logs/",
        reload=settings.DEV_MODE,
        use_colors=True,
    )



if __name__ == "__main__":
    run()  