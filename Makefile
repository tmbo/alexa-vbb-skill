.PHONY: clean deploy

help:
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    deploy"
	@echo "        Uploades code to amazon lambda."

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build
	rm -rf .serverless
	rm -rf .requirements

deploy:
	serverless deploy

