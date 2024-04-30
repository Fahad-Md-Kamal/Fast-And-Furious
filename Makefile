dev-start:
	docker compose -f docker-compose.yaml up
	@echo "------------------------"


help:
	@echo "\n\n"
	@echo "------------------------------------------"
	@echo "########## Available commands: ##########"
	@echo "------------------------------------------"
	@echo "\n\n"
	@echo "dev-start  ---->  start development environment"
	@echo "\n\n"