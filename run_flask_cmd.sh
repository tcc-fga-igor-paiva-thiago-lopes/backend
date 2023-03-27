
docker exec -it truck_app_web bash -c "cd src/ && python3 -m flask --app 'app:create_app(False)' $1"
