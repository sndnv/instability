# instability

Simple network latency and speed collection service with a web UI for displaying collected data.

## Data collection

#### Latency
Based on *ping* and provides:

* `loss` - percentage of lost packets
* `average` - average latency to target host (in milliseconds)
* `minimum` - minimum latency to target host (in milliseconds)
* `maximum` - maximum latency to target host (in milliseconds)

#### Speed
Based on *speedtest.net* and provides:

* `download` - download speed (in bits per second)
* `upload` - upload speed (in bits per second)
* `server` - server used for performing the test

## Web UI
By default, the web UI can be accessed at `http://localhost:8000`.

## Prometheus
By default, the Prometheus metrics endpoint can be accessed at `http://localhost:9000`.

## Docker

`docker pull sndnv/instability`

#### Configuring

| Environment Variables         | Description                                   | Defaults                      |
|-------------------------------|-----------------------------------------------|-------------------------------|
| `LOG_LEVEL`                   | Logging Level                                 | `DEBUG`                       |
| `DATA_STORE`                  | Path to SQLite database file                  | `store.db`                    |
| `SERVICE_HOST`                | Hostname for binding the web UI service       | `localhost`                   |
| `SERVICE_PORT`                | Port for binding the web UI service           | `8000`                        |
| `PROMETHEUS_HOST`             | Hostname for binding the Prometheus service   | `localhost`                   |
| `PROMETHEUS_PORT`             | Port for binding the Prometheus service       | `9000`                        |
| `LATENCY_TARGETS`             | List of hosts to use for latency queries      | `""` (*comma-separated list*) |
| `LATENCY_COLLECTION_INTERVAL` | Latency data collection interval              | `60` (*in seconds*)           |
| `SPEED_COLLECTION_INTERVAL`   | Speed data collection interval                | `3600` (*in seconds*)         |

#### Running with `docker`

```
docker run \
    -e LATENCY_TARGETS='192.168.1.1,8.8.8.8,google.com' \
    -e SERVICE_HOST='0.0.0.0' \
    -e PROMETHEUS_HOST='0.0.0.0' \
    -e SERVICE_PORT='5000' \
    -e LATENCY_COLLECTION_INTERVAL='30' \
    -p 9000:5000 \
    sndnv/instability
```

> Starts the service with hosts for latency queries `192.168.1.1`, `8.8.8.8` and `google.com`; with latency collection interval of `30 seconds`, default speed connection interval (`1 hour`) and binds the web UI to port `5000` (inside the container) and port `9000` (on the host).

#### Running with `docker-compose`

`cd ./example && docker-compose up`

> Uses the example `docker-compose.yml` file to start [prometheus](https://prometheus.io/) (`http://localhost:9090`), [grafana](https://grafana.com/) (`http://localhost:3000`) and `instability` (`http://localhost:8000`).

## Versioning
We use [SemVer](http://semver.org/) for versioning.

## License
This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details

> Copyright 2018 https://github.com/sndnv
>
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
>
> http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.
