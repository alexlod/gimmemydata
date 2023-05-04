# Gimme My Data!

A utility app for gathering my personal data from all the various services I use and then saving it in S3 / Postgres.   Securely.  

<img src="https://user-images.githubusercontent.com/2133615/235820536-2ce17b67-608c-46b3-9806-f41dd56e8721.png" width="700">

# Usage

Start by running `python3 manage.cli --config` to configure your client credentials for the datasources you want to pull from.  Currently the only options are to use AWS S3 for storage, so you'll need to create one of those and specify it in your config.yaml as well.   Postgres is used for storing auth credentials and some lightweight task logging. 

Modify `manage/deploy.py` to set your preferred cron job frequency for the various data collection tasks.

Once configuration is complete, you can run the application locally using the following cli commands:
- `python3 manage.cli deploy` - Run the `manage/deploy.py' script.  It will ensure previously set cron jobs will be removed before deploying new ones.
- `python3 manage.cli list` - List currently running tasks.
- `python3 manage.cli clear` - Clear any currently live cron jobs. 


## TODO: 
- standardize oauth auth flow (code to token to db, etc.) across datasources.
- Add simple UI for managing integrations and auth flows
- finish spotify features functionality.   have the program save an s3 key for each new track id.   like s3://gimmemydata/spotify/tracks/features/<track_id>.json.   Have the program go check and see if we already have the features for that track or not.  if not, save one.  if yes, move on.  
- Add new API integrations
- obsidian - implement local?  Or require making the vault a private repo on github?  TBD...   Maybe it could even be an obsidian plugin that can be installed to upload stats to github, a DB, or to s3?
- add batch interface for datasources without api's (e.g. Audible, Goodreads)
- finish schema explorer.   Potentially add schema-registry tool.
- potentially overhaul the data model and see if we can standardize it more.  

## Supported API Sources
- Oura: https://cloud.ouraring.com/v2/docs#section/Overview
- Strava: https://developers.strava.com/docs/reference/#api-Activities-getLoggedInAthleteActivities
- Spotify: https://developer.spotify.com/documentation/web-api
- Github: https://docs.github.com/en/rest?apiVersion=2022-11-28

## Coming Eventually...
- Google: we may need to use batch upload route.  
- Audible - will have to be batch
- Slack
- Apple
- Goodreads - will have to be batch (boo, Amazon!!!)