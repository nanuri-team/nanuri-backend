# 프로젝트 셋업 가이드

## 준비물

- Python 3.9
 
**pyenv** 또는 **Anaconda** 등을 사용해서 파이썬 3.9 버전을 준비해주세요.


## 서버 실행하기

1. 리포지토리를 클론합니다.

   ```
   $ git clone https://github.com/nanuri-team/nanuri-backend.git
   ```

2. 프로젝트 디렉터리에 접근합니다.

   ```
   $ cd nanuri-backend
   ```

3. 파이썬 가상환경을 만들고 활성화합니다.

   python-venv:
   ```
   $ python3 --version
   3.9.10
   
   $ python3 -m venv venv
   $ source venv/bin/activate
   ```
   
   anaconda:
   ```
   $ conda create -n nanuri-backend python=3.9
   $ conda activate nanuri-backend
   ```

4. 패키지를 설치합니다.

   ```
   $ pip install --upgrade pip setuptools wheel
   $ pip install -r requirements/local.txt
   ```

5. 데이터베이스를 생성합니다. (`db.sqlite3` 파일을 생성함)

   ```
   $ python manage.py migrate
   ```
   
6. 환경설정 템플릿 파일을 복사한 뒤 값을 설정합니다.

   ```
   $ cp .env.example .env
   ```
   
   .env:
   ```
   SECRET_KEY=<비밀 키 입력>  # https://miniwebtool.com/django-secret-key-generator/
   ```

8. 다음 명령어를 실행하여 서버가 잘 동작하는지 확인합니다.

   ```
   $ python manage.py runserver
   ```


## 데이터베이스 접근

https://sqlitebrowser.org/ 사이트에서 DB Browser for SQLite 프로그램을 다운로드 받아 설치한 뒤,
`db.sqlite3` 파일을 열면 됩니다.
