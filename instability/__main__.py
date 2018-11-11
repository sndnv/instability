from instability.collection.Service import Service as CollectionService
from instability.ui.Service import Service as UIService
from threading import Thread
import logging
import os


def main():
    logging.basicConfig(
        format='[%(asctime)-15s] [%(levelname)s] [%(name)-5s]: %(message)s',
        level=logging.DEBUG
    )

    targets = [target.strip() for target in os.getenv("LATENCY_TARGETS", "").split(",")]
    interval = os.getenv("COLLECTION_INTERVAL", 60)

    collection_service = CollectionService(db="store.db", targets=targets, collection_interval=interval)
    ui_service = UIService(db="store.db", host="localhost", port=8000)

    collection_thread = Thread(target=collection_service.start)
    collection_thread.start()

    ui_service.start()


if __name__ == "__main__":
    main()
