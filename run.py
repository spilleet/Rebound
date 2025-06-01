from app import create_app, db
from app.models import User, Court, Game, GameParticipant
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Court': Court,
        'Game': Game,
        'GameParticipant': GameParticipant
    }

if __name__ == '__main__':
    # 개발 환경에서만 Flask 내장 서버 사용
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)
    else:
        # 프로덕션에서는 gunicorn이 직접 app을 실행
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False) 