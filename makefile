TEST_USR=drBaloo
TEST_MSG="Lorem ipsum"

run:
	python src/main.py --username $(TEST_USR) --message $(TEST_MSG)
