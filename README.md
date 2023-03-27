Create virtual environment:
    python3 -m venv eastvantage

Activate virtual environment:
    source eastvantage/bin/activate

Create run.sh shell file
    paste below command on that file
    uvicorn main:app --reload --port 8006

Then run below command
    chmod +x run.sh 
    
Run project
   ./run.sh 

Use the below command to install the requirements.txt file if you face any issues
    pip3 install -r requirements.txt 

Use the below command using export installed commands from our project setup
    pip3 freeze >> requirements.txt

If any log file error then create log file under logs
    logs/eastvantage.log


geopy

/********** API description ******************/
1.  Url: http://127.0.0.1:8006/api/v1/user/address?skip=0&limit=100
    Method: Get
    Description: This api is used to list all the address details in db.

2.  Url: http://127.0.0.1:8006/api/v1/user/address
    Method: Post
    Description: This api is used to create address.

3.  Url: http://127.0.0.1:8006/api/v1/user/address/{id}
    Method: put
    Description: This api is used update perticular address based on id.

4.  Url: http://127.0.0.1:8006/api/v1/user/address/{id}
    Method: put
    Description: This api is used delete perticular address based on id.

5.  Url: http://127.0.0.1:8006/api/v1/user/address_by_distance?address={address}&distance={distance}
    Method: Get
    Description: This api is used to get all the nearest available location based on given address with distance limit.
