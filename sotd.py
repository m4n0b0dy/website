import pygsheets
import pandas as pd
from datetime import date
import git
import os
import sys

#git stuff
repo = git.Repo('../website')
repo.git.checkout('gh-pages')
repo.git.pull()
#gsheets login stuff
gc = pygsheets.authorize(service_file='../client_ser_sec.json')
gc_sh = gc.open_by_key('1IUi_Qy_PHxiopgHWNeiX3lYjeNjYsg2Gi8TYdP9qfiA')
wks = gc_sh[0]
df = wks.get_as_df()
sotd_df = df[list(filter(None, list(df)))]

if len(sys.argv)==2:
    tod = date.strptime(sys.argv[1], '%y-%m-%d')
else:
    tod = date.today()

song_comps = sotd_df[sotd_df['day'] == tod.strftime("%#m/%#d/%Y")].to_dict('records')[0]

if str(song_comps['name']) == 'NaN':
    print('--No song has been added--')
    sys.exit()

if tod.timetuple().tm_yday % 2:
    song_comps['dir'] = 'r'
    song_comps['day'] = ' -- '+song_comps['day']
else:
    song_comps['dir'] = 'l'
    song_comps['day'] = song_comps['day']+' -- '

header = '''<!-- PYTHON AUTO ADD ;)-->
'''
song_html = '''<li><a href="{link}" target="_blank"><div class="icon {genre}"></div><div class="{genre}">
    <div class="direction-{dir}">
      <div class="flag-wrapper">
        <span class="flag">{name}</span>
        <span class="time-wrapper"><span class="time">{day}</span></span>
      </div>
      <div class="desc">{artist}</div>
    </div>
  </div>
</a></li>
'''.format(**song_comps)
html = header + song_html

blog = 'song_ot_day_blog.html'
with open(blog, 'r') as file :
    filedata = file.read()
    
ans = 'y'
if song_html in filedata:
    print(song_comps['name'], 'already added to SOTD.')
    sys.exit()
elif song_comps['name'] in filedata:
    ans = input('Already have %s in SOTD, add anyway?(y) '%song_comps['name']).lower()
if ans == 'y':
    filedata = filedata.replace('<!-- PYTHON AUTO ADD ;)-->', html)
    
with open(blog, 'w') as file:
    file.write(filedata)
    
repo.git.add('*')
repo.git.commit(m="sotd_for_"+str(tod))
repo.git.push('origin', 'gh-pages')
print(song_comps['name'], 'pushed!')