import os
os.environ['DATABASE_URL']='sqlite:///./test_taskflow_v2.db'
os.environ['SECRET_KEY']='test-secret'
from fastapi.testclient import TestClient
from backend.main import app

client=TestClient(app)

def test_auth_and_crud():
    email='test@example.com'
    r=client.post('/auth/register',json={'name':'Test User','email':email,'password':'password123'})
    assert r.status_code==201
    token=r.json()['access_token']; h={'Authorization':f'Bearer {token}'}
    r=client.post('/projects',json={'name':'Demo','description':'Test'},headers=h); assert r.status_code==201
    pid=r.json()['id']
    r=client.post('/tasks',json={'title':'Write tests','priority':'high','status':'pending','project_id':pid},headers=h); assert r.status_code==201
    tid=r.json()['id']
    r=client.put(f'/tasks/{tid}',json={'status':'completed'},headers=h); assert r.status_code==200 and r.json()['status']=='completed'
    r=client.get('/tasks',headers=h); assert r.status_code==200 and len(r.json())==1
    r=client.get('/tasks/search',params={'title':'Write tests','algo':'binary'},headers=h); assert r.status_code==200
    r=client.delete(f'/tasks/{tid}',headers=h); assert r.status_code==200
