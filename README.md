# qbestd_box

## All-in-one Docker container for deploying a Query-by-Example Spoken Term Detection system

### Usage

1. Clone this GitHub repository

	```bash
	git clone https://github.com/parledoct/qbestd_box.git
	cd qbestd_box
	```

2. Set up environment:

	a. Use supplied docker container (recommended):
	
	```bash
	# Launch parledoct/qbestd_box container with 
	# settings defiend in docker-compose.yml
	docker-compose run --rm search
	```

	b. Or set up your local environment with required packages:

	```bash
	pip install -r requirements.txt
	```

3. Run a search using `qbestd.py`

	Run a search using the `gos-kdl_queries` collection (`0375ff...`) as queries and `gos-kdl_corpus` as test items (`3e2d65...`); for collection IDs see `data/sqlite/collection_names.csv`.

	```bash
	python qbestd.py \
		--progress \
		--concurrent \
		0375ff9c2d8555e88be65079d6c42df3 \
		3e2d65d4486b2059ec9802a4221aacc0
	```

	You can use `python qbestd.py -h` for usage instructions:
	
	```bash
	usage: qbestd.py [-h] [-p] [-c] [-w MAX_WORKERS] query_id test_id

	example: python qbest.py c4f0f58d1af2223da0519dc0496e7600 afeb2b96e36f1b38548959b3494a91e7

	positional arguments:
	  query_id              Identifier for a query features file or a query collection.
	  test_id               Identifier for a test item features file or a test item collection.

	optional arguments:
	  -h, --help            show this help message and exit
	  -p, --progress        show progress bar. (default: False)
	  -c, --concurrent      run DTW searches concurrently. (default: False)
	  -mw MAX_WORKERS, --max_workers MAX_WORKERS
	                        if running concurrent jobs, maximum number of workers (None = use all available cores) (default: None)
	```
	
	