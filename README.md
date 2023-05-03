# Gimme My Data!

A utility for gathering my personal data from public APIs and saving it in S3 & Postgres.   

<img src="https://user-images.githubusercontent.com/2133615/235820536-2ce17b67-608c-46b3-9806-f41dd56e8721.png" width="700">


## Links to Source API Documentation
- Oura: https://cloud.ouraring.com/v2/docs#section/Overview
- Strava: https://developers.strava.com/docs/reference/#api-Activities-getLoggedInAthleteActivities
- Spotify: https://developer.spotify.com/documentation/web-api
- Github: https://docs.github.com/en/rest?apiVersion=2022-11-28
- Google: 



## TODO: 
- finish spotify features functionality.   have the program save an s3 key for each new track id.   like s3://gimmemydata/spotify/tracks/features/<track_id>.json.   Have the program go check and see if we already have the features for that track or not.  if not, save one.  if yes, move on.  
