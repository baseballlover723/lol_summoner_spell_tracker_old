# Various Development Architecture Stuff

## Data Models & Data Transfer Objects
### Data Models
#### summoner:
id | id (summoner_id)

username | string

region | enum

last_updated | datetime

alias summoner_id to id

#### champion
name | string

image_url | url

#### summoner_spell
id | int

name | string

image_url | url

base_cooldown | int (seconds)

#### ult_cd (optional) (not in v1)
champion_id | id
level | int < 18
base_cooldown | int (seconds)

### Data Transfer Objects
#### summoner_champion
summoner | fill(summoner_id)

champion | fill(champion_id)

summoner_d | fill(summoner_d_id)

summoner_f | fill(summoner_f_id)

summoner_cooldown_from_runes: int (%)

#### current_match

blue_team | [current_match_summoner_champion x 5]

red_team | [current_match_summoner_champion x 5]

region | string

queue_type | string


```python
def init(region, queue_type):
    @blue_team = []
    @red_team = []
    @region = region
    @queue_type = queue_type

def add_blue_side_summoner(db_summoner):
    ...
    
def add_red_side_summoner(db_summoner):
    ...

```


## Outline of API Calls
### helpers
```python
def get_summoner(region, id or username):
    summoner = Summoner.find_by(region: region, id or username)
    if (!summoner or summoner.stale?)
        new_summoner = repull_summoner(summoner)
        persist_summoner(new_summoner)
        summoner = new_summoner
     return summoner

def calculate_cd_from_runes(raw_summoner.runes):
    ...
    
    return int # %
```

### /:region/:summoner_username (live_game)
```python
current_summoner = get_summoner(region, username)

raw_current_match = get_current_match(region=region, summoner_id=summoner.id)
current_match = new CurrentMatch(region=region, queue_type=raw_current_match.queue_type)
for (raw_summoner in raw_current_match.summoners)
    summoner = get_summoner(region, raw_summoner.id)
    champion = get_champion(raw_summoner.champion_id)
    summoner_d = SummonerSpell.find(raw_summoner.summoner_d_id)
    summoner_f = SummonerSpell.find(raw_summoner.summoner_f_id)
    ss_cd = calculate_cd_from_runes(raw_summoner.runes)
    summoner_chamption = new SummonerChampion(summoner, champion, summoner_d, summoner_f, ss_cd)
    if (raw_summoner.blue_side?)
        current_match.add_blue_side_summoner(summoner)
    else        
        current_match.add_red_side_summoner(summoner)
render json: current_match
```
