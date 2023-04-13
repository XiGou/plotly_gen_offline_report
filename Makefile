ASSETS_DIR=plotly_offline_report/assets
.PHONY: get_static_assets
get_static_assets:
	if [ ! -d ${ASSETS_DIR} ]; then mkdir ${ASSETS_DIR}; fi
	if [ ! -f ${ASSETS_DIR}/bootstrap.bundle.min.js ]; then \
		wget https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.2/js/bootstrap.bundle.min.js \
		-O ${ASSETS_DIR}/bootstrap.bundle.min.js;\
	fi
	if [ ! -f ${ASSETS_DIR}/bootstrap.min.css ]; then \
		wget https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.2/css/bootstrap.min.css \
		-O ${ASSETS_DIR}/bootstrap.min.css; \
	fi
	if [ ! -f ${ASSETS_DIR}/__init__.py ]; then touch ${ASSETS_DIR}/__init__.py; fi


.PHONY: test
test: clean get_static_assets
	python3 -m unittest tests/test_gen_report.py

.PHONY: clean
clean:
	rm -rf /tmp/plotly_gen_report

.PHONY: format
format:
	black .