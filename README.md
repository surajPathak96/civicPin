# Full project description 
Problem: Civic issues like waterlogged roads and blocked drains are noticed by many people but logged by none. There is no lightweight way to see what is reported in an area and what is still unresolved.

# How to run (the venv, install, and uvicorn steps from setup).

## make a venv file first-->
python3 -m venv venv

### To activate venv use command given below 
source venv/bin/activate    


# How to install Fastapi on venv use this command 
pip install fastapi "uvicorn[standard]" python-multipart

# To execute whole project 
python uvicorn -m main:app --reload



# The API contract: today’s two endpoints with example JSON, plus the planned ones marked TODO (P1), TODO (P2), TODO (P3) per the slice table
