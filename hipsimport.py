import hipscat_import.pipeline as runner
from hipscat_import.pipeline import pipeline_with_client
from dask.distributed import LocalCluster, Client
import yaml
from sys import argv
import dask.config
import dask.distributed

dask.config.set({"array.chunk-size": "128 MiB"})
dask.config.set({"distributed.workers.memory.spill": 0.90})
dask.config.set({"distributed.workers.memory.target": 0.80})
dask.config.set({"distributed.workers.memory.terminate": 0.98})
dask.config.set({"distributed.nanny.environ.MALLOC_TRIM_THRESHOLD_": 0})


def get_config():
    if len(argv) > 1:
        config_file = argv[1]
    else:
        raise ValueError("No config")

    with open(config_file, 'r') as _file:
        params = yaml.safe_load(_file)

    return params


def main():
    params = get_config()

    args = runner.ImportArguments(**params)
    memlim = "%iGB" % round(125 / int(args.dask_n_workers))

    cluster = LocalCluster(
        n_workers=args.dask_n_workers,
        local_directory=args.dask_tmp,
        threads_per_worker=args.dask_threads_per_worker,
        memory_limit=memlim
    )
    with Client(cluster) as client:
        pipeline_with_client(args, client)


if __name__ == "__main__": main()
