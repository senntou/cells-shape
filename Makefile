all :
	python3 src/main.py

clean :
	rm -rf output

test :
	pytest tests/*.py
