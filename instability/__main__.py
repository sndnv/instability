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
    latency_interval = os.getenv("LATENCY_COLLECTION_INTERVAL", 60)
    speed_interval = os.getenv("SPEED_COLLECTION_INTERVAL", 60 * 60)

    collection_service = CollectionService(
        db="store.db", targets=targets,
        latency_collection_interval=latency_interval,
        speed_collection_interval=speed_interval
    )

    ui_service = UIService(db="store.db", host="localhost", port=8000)

    latency_collection_thread = Thread(target=collection_service.start_latency_collection)
    latency_collection_thread.start()

    speed_collection_thread = Thread(target=collection_service.start_speed_collection)
    speed_collection_thread.start()

    ui_service.start()


if __name__ == "__main__":
    main()
