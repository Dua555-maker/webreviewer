genres = [
  'Action','Horror','Sci-Fi','Fantasy','Western','Romance','Thriller','Comedy',
  'Drama','Apocalypse','Martial Arts','Sports'
]

from webreview.models import TypeMovie
from webreview.extensions import db
def create_movie_genres():
  for genre in genres:
    mg = TypeMovie(name=genre)
    db.session.add(mg)
  db.session.commit()