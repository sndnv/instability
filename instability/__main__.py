from instability.collection.Service import Service as CollectionService
from instability.persistence.SQLite import SQLite
from instability.ui.Service import Service as UIService
from threading import Thread
import logging
import os


def main():
    log_level = os.getenv("LOG_LEVEL", "DEBUG")
    logging.basicConfig(
        format='[%(asctime)-15s] [%(levelname)s] [%(name)-5s]: %(message)s',
        level=logging.getLevelName(log_level)
    )

    data_store = os.getenv("DATA_STORE", "store.db")
    service_host = os.getenv("SERVICE_HOST", "localhost")
    service_port = int(os.getenv("SERVICE_PORT", 8000))
    targets = [target.strip() for target in os.getenv("LATENCY_TARGETS", "").split(",")]
    latency_interval = int(os.getenv("LATENCY_COLLECTION_INTERVAL", 60))
    speed_interval = int(os.getenv("SPEED_COLLECTION_INTERVAL", 60 * 60))

    collection_service = CollectionService(
        db="store.db", targets=targets,
        latency_collection_interval=latency_interval,
        speed_collection_interval=speed_interval
    )

    with SQLite(data_store) as store:
        if not store.latency_table_exists():
            store.latency_table_create()

        if not store.speed_table_exists():
            store.speed_table_create()

    ui_service = UIService(db=data_store, host=service_host, port=service_port)

    if latency_interval > 0:
        latency_collection_thread = Thread(target=collection_service.start_latency_collection)
        latency_collection_thread.start()
    else:
        logging.warning("Collection of latency data disabled")

    if speed_interval > 0:
        speed_collection_thread = Thread(target=collection_service.start_speed_collection)
        speed_collection_thread.start()
    else:
        logging.warning("Collection of speed data disabled")

    ui_service.start()


if __name__ == "__main__":
    main()
