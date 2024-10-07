image:
	docker build . -t hsiangjenli/sphinx-doc:scsb-base -f Dockerfile.sphinx 

mkdocs:
	docker run -it --rm -v "$(PWD):/docs" hsiangjenli/sphinx-doc:scsb-base bash -c "pip install . && cd docs && make html"