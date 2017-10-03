#python flask_raas.py mongodb://127.0.0.1/verce-prov True
#gunicorn -w 4 -b 127.0.0.1:8082 flask_raas:app 
export RAAS_LOGGING="True"
export RAAS_REPO="mongodb://127.0.0.1/$SPROV_DB"
gunicorn -w 9 -b 127.0.0.1:8082 "flask_raas:bootstrap_app()" --log-level debug --backlog 0 --timeout 120 --error-logfile error.log --log-file access.log &
