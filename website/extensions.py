from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 

login_manager = LoginManager()
db = SQLAlchemy()

TEAMS = set(['North Dakota', 'AIC', 'Minnesota Duluth', 'Michigan', 'Wisconsin', 'Bemidji State', 
        'Lake Superior State', 'Massachusetts', 'Minnesota', 'Omaha', 'Minnesota State', 
        'Quinnipiac', 'Boston College', 'Notre Dame', 'St. Cloud State', 'Boston University'])