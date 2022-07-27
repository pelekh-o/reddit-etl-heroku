# reddit-etl-heroku

Heroku version of the [reddit-etl](https://github.com/pelekh-o/reddit-etl) project


## Deploying to Heroku
0. Create an account on [Heroku](https://www.heroku.com/)
1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Go to Heroku website and create a new app
3. Go to Settings ➜ Add buildpack ➜ python
4. ```cd``` to project's root directory and run 
```commandline
echo "web: python main.py  
worker: python main.py" >> Procfile
```
