# Gimme My Data!

A utility for gathering my personal data from public APIs and saving it in S3 & Postgres.   

![image](https://user-images.githubusercontent.com/2133615/235820536-2ce17b67-608c-46b3-9806-f41dd56e8721.png | width=700)


## Source API Docs
- Oura: https://cloud.ouraring.com/v2/docs#section/Overview
- Strava: https://developers.strava.com/docs/reference/#api-Activities-getLoggedInAthleteActivities
- Spotify: https://developer.spotify.com/documentation/web-api



## TODO: 
- finish spotify features functionality.   have the program save an s3 key for each new track id.   like s3://gimmemydata/spotify/tracks/features/<track_id>.json.   Have the program go check and see if we already have the features for that track or not.  if not, save one.  if yes, move on.  
