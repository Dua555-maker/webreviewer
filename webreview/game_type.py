genres = [
  'Action','Adventure','Horror','RPG','Strategy','Fighting','Puzzle','Racing',
  'Sports','Shooter','Platformer','Simulation','Survival','Sandbox','Educational'
]

from webreview.models import TypeGame
from webreview.extensions import db
def create_game_genres():
  for genre in genres:
    gg = TypeGame(name=genre)
    db.session.add(gg)
  db.session.commit()