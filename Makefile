all :
	python3 src/main.py

clean :
	rm -rf output
	rm -rf output_whole

test :
	pytest tests/*.py -s

cache-clear : 
	rm -rf cache

serve:
	streamlit run server/server.py --server.address localhost --server.port 8505


