from typing import TypedDict
from typing import Collection, Dict, Optional, Union
from modal import Image, Secret, Mount, SharedVolume, Proxy
from modal.gpu import GPU_T


class Config_Stub(TypedDict):
    label: str  # Label for created endpoint. Final subdomain will be <workspace>--<label>.modal.run.
    wait_for_response: bool  # Whether requests should wait for and return the function response.
    image: Image  # The image to run as the container for the function
    secret: Optional[Secret]  # An optional Modal Secret with environment variables for the container
    secrets: Collection[Secret]  # Plural version of `secret` when multiple secrets are needed
    gpu: GPU_T  # GPU specification as string ("any", "T4", "A10G", ...) or object (`modal.GPU.A100()`, ...)
    mounts: Collection[Mount]
    shared_volumes: Dict[str, SharedVolume]
    cpu: Optional[float]  # How many CPU cores to request. This is a soft limit.
    memory: Optional[int]  # How much memory to request, in MB. This is a soft limit.
    proxy: Optional[Proxy]  # Reference to a Modal Proxy to use in front of this function.
    retries: Optional[int]  # Number of times to retry each input in case of failure.
    concurrency_limit: Optional[int]  # Limit for max concurrent containers running the function.
    container_idle_timeout: Optional[int]  # Timeout for idle containers waiting for inputs to shut down.
    timeout: Optional[int]  # Maximum execution time of the function in seconds.
    keep_warm: Union[bool, int]  # Toggles an adaptively-sized warm pool for latency-sensitive apps.
    cloud: Optional[str]  # Cloud provider to run the function on. Possible values are aws, gcp, auto.


class Config(TypedDict):
    log: bool
    stub: Config_Stub
