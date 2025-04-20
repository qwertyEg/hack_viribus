import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from vector_store import VectorStore
import os

class PDFHandler(FileSystemEventHandler):
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.pdf'):
            print(f"Новый PDF файл обнаружен: {event.src_path}")
            self.vector_store.add_documents(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.pdf'):
            print(f"PDF файл изменен: {event.src_path}")
            self.vector_store.add_documents(event.src_path)

class Watcher:
    def __init__(self, path_to_watch: str, vector_store: VectorStore):
        self.path_to_watch = path_to_watch
        self.vector_store = vector_store
        self.event_handler = PDFHandler(vector_store)
        self.observer = Observer()

    def run(self):
        print(f"Начинаю отслеживать изменения в директории: {self.path_to_watch}")
        self.observer.schedule(self.event_handler, self.path_to_watch, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Остановка отслеживания...")
        self.observer.join()
