# Setup

1. Run

   ```
   export FLASK_CONFIG="config.py"
   ```

2. Install `VirtualEnv` with

   ```
   pip install virtualenv
   ```

3. Create a VirtualEnv and use the virtual env

   ```
   virtualenv venv
   ```

   then

   ```
   source venv/bin/activate
   ```

4. Install requirements

   ```
   venv/bin/pip install -r requirements.txt
   ```

To run seed file

```
venv/bin/python3 -m app.seed
```

To run flask server

```
venv/bin/python3 -m app.run
```

# Database schema

![FYPD-database-schema-1](https://user-images.githubusercontent.com/34842935/148301721-68144e48-1a5a-49b1-bf59-7742554e82f6.png)
