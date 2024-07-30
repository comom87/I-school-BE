from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_correct_post():
    timetable_id = 1
    course_code = "CS101"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    #print(response.json())
    assert response.json() == {"success" : True, "data" : None, "error" : None}
    

def test_correct_timetable_incorrect_coursecode_post():
    timetable_id = 1
    course_code = "Bad Course Code"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {'success': False, 'data': None, 'error': '강의가 존재하지 않습니다.'}


def test_incorrect_timetable_correct_coursecode_post():
    timetable_id = 4
    course_code = "CS101"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {'success': False, 'data': None, 'error': "시간표가 존재하지 않습니다."}

def test_incorrect_timetable_incorrect_coursecode_post():
    timetable_id = 4
    course_code = "Bad Course Code"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {'success': False, 'data': None, 'error': "시간표가 존재하지 않습니다."}


