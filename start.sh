sudo /usr/bin/python3 -m frame_description_app &
sudo /usr/bin/python3 garbage_collector.py &
sudo /usr/bin/python3 -m streamlit run Home.py --server.port 80