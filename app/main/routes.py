from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.main import bp
from app.models import Game, Court, GameParticipant
from app import db

@bp.route('/')
@bp.route('/index')
def index():
    games = Game.query.all()
    courts = Court.query.all()
    return render_template('main/index.html', 
                         title='메인 페이지',
                         games=games,
                         courts=courts)

@bp.route('/mypage')
@login_required
def mypage():
    participated_games = GameParticipant.query.filter_by(user_id=current_user.id).all()
    created_games = Game.query.filter_by(creator_id=current_user.id).all()
    return render_template('main/mypage.html',
                         title='마이페이지',
                         participated_games=participated_games,
                         created_games=created_games)

@bp.route('/join_game/<int:game_id>')
@login_required
def join_game(game_id):
    game = Game.query.get_or_404(game_id)
    
    # 이미 참가 신청한 경우 체크
    if GameParticipant.query.filter_by(game_id=game_id, user_id=current_user.id).first():
        flash('이미 참가 신청한 경기입니다.')
        return redirect(url_for('main.index'))
    
    # 본인이 만든 경기인 경우 체크
    if game.creator_id == current_user.id:
        flash('본인이 만든 경기에는 참가 신청할 수 없습니다.')
        return redirect(url_for('main.index'))
    
    # 최대 인원 초과 체크
    if game.participants.count() >= game.max_players:
        flash('이미 최대 인원에 도달했습니다.')
        return redirect(url_for('main.index'))
    
    # 참가 신청 처리
    participant = GameParticipant(game_id=game_id, user_id=current_user.id)
    db.session.add(participant)
    db.session.commit()
    
    flash('경기 참가 신청이 완료되었습니다.')
    return redirect(url_for('main.mypage'))

@bp.route('/join_selected_games', methods=['POST'])
@login_required
def join_selected_games():
    selected_games = request.form.getlist('selected_games')
    
    if not selected_games:
        flash('선택된 경기가 없습니다.')
        return redirect(url_for('main.index'))
    
    success_count = 0
    for game_id in selected_games:
        game = Game.query.get(game_id)
        if game and game.creator_id != current_user.id:
            if not GameParticipant.query.filter_by(game_id=game_id, user_id=current_user.id).first():
                if game.participants.count() < game.max_players:
                    participant = GameParticipant(game_id=game_id, user_id=current_user.id)
                    db.session.add(participant)
                    success_count += 1
    
    if success_count > 0:
        db.session.commit()
        flash(f'{success_count}개의 경기 참가 신청이 완료되었습니다.')
    else:
        flash('참가 신청할 수 있는 경기가 없습니다.')
    
    return redirect(url_for('main.mypage')) 