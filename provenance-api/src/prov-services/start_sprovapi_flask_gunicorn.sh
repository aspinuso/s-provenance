export SPROV_LOGGING="True"
export SPROV_REPO="mongodb://127.0.0.1/verce-prov"
gunicorn -w 9 -b 127.0.0.1:8082 "sprovflow_api:bootstrap_app()" --log-level debug --backlog 0 --timeout 120 --error-logfile error.log --log-file access.log &
