# RUN FLASK APP

To run the application, use the `flask` command, you need to tell the Flask where your application is with the
`--app` option

```python
flask -- app <file name> run

#or

python -m flask
```

## Routing

Use the `route()` decorator to bind a function to a URL

```python
@app.route('/hello') # /hello need to be typed in browser to redirect to this path
    return 'Index Page'
```

### Variable rules

You can add variable sections to a URL by marking sections with <variable_name>. The function then receive
the <variable_name> as argument.
A <converter:variable_name> can be used to specify the type of the argument

```python
@app.route('/user/<username>')
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
```

#### Static files

To generate URLs for static files, use the special `'static'` endpoint name:

```python
url_for('static', filename='style.css')
```

The file has to be stored on the filesystem as static/style.css
