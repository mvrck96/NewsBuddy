
echo --------------------------- Create Prefect blocks -----------------------------------------------
python ./NewsBuddy/api_manager/orchestration/create_blocks.py
echo --------------------------- Create Prefect deployment for /NewsBuddy/api_manager/fetch_news.py ---------------------
python ./NewsBuddy/api_manager/orchestration/flows/fetch_news.py
# cd ./NewsBuddy/api_manager/orchestration/flows && python fetch_news.py && cd ~
echo ------ One can run \"prefect deployment run fetch-news/main\" to trigger the deployment run
