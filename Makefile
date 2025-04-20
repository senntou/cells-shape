all :
	python3 src/main.py

clean :
	rm -rf output
	rm -rf output_whole

test :
	pytest tests/*.py -s
